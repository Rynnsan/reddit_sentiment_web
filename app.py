import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import praw
from datetime import datetime
import random

load_dotenv()

app = Flask(__name__)

# Reddit API bağlantısı
reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT"),
)

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
def analyze(subreddit):
    try:
        subreddit_obj = reddit.subreddit(subreddit)
        posts = []
        
        # Subreddit'in var olup olmadığını kontrol et
        try:
            subreddit_obj.id  # Bu satır subreddit'in var olup olmadığını kontrol eder
        except Exception:
            return jsonify({"error": f"Subreddit '{subreddit}' not found or private"}), 404
        
        # Hot posts'ları al
        for post in subreddit_obj.hot(limit=10):
            # Rastgele sentiment değeri ata (gerçek sentiment analizi için değiştirilebilir)
            sentiment_options = ["positive", "neutral", "negative"]
            sentiment = random.choice(sentiment_options)
            
            posts.append({
                "title": post.title,
                "score": post.score,
                "comments": post.num_comments,
                "timestamp": datetime.utcfromtimestamp(post.created_utc).strftime("%Y-%m-%d %H:%M:%S"),
                "url": post.url,
                "sentiment": sentiment
            })

        # Örnek sentiment değerleri
        positive = random.randint(25, 50)
        negative = random.randint(15, 35)
        neutral = 100 - positive - negative

        # Örnek trending keywords
        sample_keywords = ["technology", "update", "news", "discussion", "help", "question", "opinion", "review"]
        trending_keywords = random.sample(sample_keywords, min(5, len(sample_keywords)))

        # Subreddit istatistikleri
        try:
            subscribers = subreddit_obj.subscribers
            active_users = random.randint(100, 5000)  # Aktif kullanıcı sayısı tahmin
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