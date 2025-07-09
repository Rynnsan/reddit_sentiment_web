import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import praw
from datetime import datetime
import random
from nlp_utils import get_sentiment_label

load_dotenv()

app = Flask(__name__)

# Reddit API bağlantısı
reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT"),
)
def get_sentiment_label(text):
    text = text.lower()
    positive_words = ['good', 'great', 'awesome', 'happy', 'love', 'excellent', 'nice']
    negative_words = ['bad', 'terrible', 'hate', 'awful', 'worst', 'sad', 'angry']
    
    pos_count = sum(word in text for word in positive_words)
    neg_count = sum(word in text for word in negative_words)
    
    if pos_count > neg_count:
        return "positive"
    elif neg_count > pos_count:
        return "negative"
    else:
        return "neutral"

# Örnek trending subreddits verisi
TRENDING_SUBREDDITS = [
    {"name": "technology", "posts": "1.2K", "sentiment": "positive"},
    {"name": "worldnews", "posts": "3.5K", "sentiment": "neutral"},
    {"name": "gaming", "posts": "2.8K", "sentiment": "positive"},
    {"name": "movies", "posts": "1.1K", "sentiment": "positive"},
    {"name": "science", "posts": "890", "sentiment": "neutral"},
    {"name": "AskReddit", "posts": "4.2K", "sentiment": "neutral"},
    {"name": "funny", "posts": "2.1K", "sentiment": "positive"},
    {"name": "pics", "posts": "1.8K", "sentiment": "positive"}
]

@app.route("/")
def home():
    return render_template("index.html", trending=TRENDING_SUBREDDITS)

@app.route("/suggest_subreddits")
def suggest_subreddits():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify([])

    try:
        # Reddit API'den subreddit önerileri al
        results = reddit.subreddits.search(query, limit=8)
        suggestions = []
        
        for sub in results:
            suggestions.append(sub.display_name)
        
        return jsonify(suggestions)
    except Exception as e:
        print(f"Error fetching suggestions: {str(e)}")
        # Hata durumunda örnek veriler döndür
        sample_suggestions = [
            "AskReddit", "worldnews", "technology", "gaming", 
            "movies", "science", "funny", "pics"
        ]
        filtered_suggestions = [s for s in sample_suggestions if query.lower() in s.lower()]
        return jsonify(filtered_suggestions[:5])

@app.route("/analyze/<subreddit>")
@app.route("/analyze/<subreddit>")
def analyze(subreddit):
    try:
        subreddit_obj = reddit.subreddit(subreddit)
        posts = []
        positive, neutral, negative = 0, 0, 0
        
        # Subreddit var mı kontrol et
        try:
            subreddit_obj.id
        except Exception:
            return jsonify({"error": f"Subreddit '{subreddit}' not found or private"}), 404
        
        # Hot postları al ve sentiment hesapla
        for post in subreddit_obj.hot(limit=10):
            sentiment = get_sentiment_label(post.title)

            if sentiment == "positive":
                positive += 1
            elif sentiment == "negative":
                negative += 1
            else:
                neutral += 1

            posts.append({
                "title": post.title,
                "score": post.score,
                "comments": post.num_comments,
                "timestamp": datetime.utcfromtimestamp(post.created_utc).strftime("%Y-%m-%d %H:%M:%S"),
                "url": post.url,
                "sentiment": sentiment
            })

        total = positive + neutral + negative or 1
        positive = round((positive / total) * 100)
        neutral = round((neutral / total) * 100)
        negative = 100 - positive - neutral

        # Trending keywords örnek
        sample_keywords = ["technology", "update", "news", "discussion", "help", "question", "opinion", "review"]
        trending_keywords = sample_keywords[:5]

        # Abone ve aktif kullanıcı bilgisi (aktif kullanıcı tahmini)
        try:
            subscribers = subreddit_obj.subscribers
            active_users = random.randint(100, 5000)
        except:
            subscribers = "N/A"
            active_users = "N/A"

        response = {
            "sentiments": {
                "positive": positive,
                "neutral": neutral,
                "negative": negative
            },
            "summary": f"Analysis of r/{subreddit} shows {positive}% positive, {neutral}% neutral, and {negative}% negative sentiment. The community appears to be {'very active' if len(posts) > 8 else 'moderately active'} with diverse discussions.",
            "total_posts": len(posts),
            "active_users": active_users,
            "sample_posts": posts,
            "trending_keywords": trending_keywords,
            "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }

        return jsonify(response)

    except Exception as e:
        print(f"Error analyzing subreddit: {str(e)}")
        return jsonify({"error": f"Failed to analyze subreddit '{subreddit}': {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)