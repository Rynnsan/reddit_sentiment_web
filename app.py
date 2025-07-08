from flask import Flask, render_template, request, jsonify
import random
from datetime import datetime, timedelta

app = Flask(__name__)

# Expanded subreddit list with categories
SUBREDDIT_LIST = [
    "AskReddit", "america", "AmericanCars", "AmateurPhotography",
    "aww", "android", "anime", "Art", "AskScience", "Bitcoin",
    "books", "cars", "cooking", "cryptocurrency", "dataisbeautiful",
    "EarthPorn", "Economics", "explainlikeimfive", "funny",
    "gaming", "history", "investing", "IAmA", "javascript",
    "LifeProTips", "movies", "music", "news", "photography",
    "politics", "programming", "science", "sports", "technology",
    "todayilearned", "videos", "worldnews", "MachineLearning",
    "stocks", "personalfinance", "fitness", "relationships"
]

# Sample trending subreddits
TRENDING_SUBREDDITS = [
    {"name": "technology", "posts": 1234, "sentiment": "positive"},
    {"name": "investing", "posts": 892, "sentiment": "negative"},
    {"name": "gaming", "posts": 2341, "sentiment": "positive"},
    {"name": "news", "posts": 1876, "sentiment": "neutral"},
    {"name": "cryptocurrency", "posts": 743, "sentiment": "negative"}
]

@app.route("/")
def home():
    return render_template("index.html", trending=TRENDING_SUBREDDITS)

@app.route("/suggest_subreddits")
def suggest_subreddits():
    query = request.args.get("q", "").lower()
    suggestions = [sub for sub in SUBREDDIT_LIST if query in sub.lower()]
    return jsonify(suggestions[:8])  # Limit to 8 suggestions

@app.route("/analyze/<subreddit>")
def analyze(subreddit):
    # Enhanced dummy response with more realistic data
    positive = random.randint(15, 45)
    negative = random.randint(10, 35)
    neutral = 100 - positive - negative
    
    # Generate sample posts data
    sample_posts = [
        {
            "title": f"Sample post from r/{subreddit} #{i+1}",
            "sentiment": random.choice(["positive", "negative", "neutral"]),
            "score": random.randint(1, 500),
            "comments": random.randint(5, 150),
            "timestamp": (datetime.now() - timedelta(hours=random.randint(1, 24))).strftime("%Y-%m-%d %H:%M")
        }
        for i in range(5)
    ]
    
    # Generate trending keywords
    trending_keywords = [
        f"keyword_{i}" for i in range(1, 11)
    ]
    
    response = {
        "sentiments": {
            "positive": positive,
            "neutral": neutral,
            "negative": negative
        },
        "summary": f"Analysis of r/{subreddit} shows {positive}% positive sentiment. The community appears to be {'optimistic' if positive > 35 else 'mixed' if positive > 25 else 'cautious'} about recent discussions.",
        "total_posts": random.randint(50, 500),
        "active_users": random.randint(100, 5000),
        "sample_posts": sample_posts,
        "trending_keywords": trending_keywords,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return jsonify(response)

@app.route("/trending")
def get_trending():
    return jsonify(TRENDING_SUBREDDITS)

@app.route("/stats/<subreddit>")
def get_stats(subreddit):
    # Mock statistics endpoint
    stats = {
        "subscribers": random.randint(10000, 1000000),
        "online_users": random.randint(100, 10000),
        "posts_today": random.randint(50, 500),
        "avg_sentiment_week": random.uniform(0.3, 0.8),
        "growth_rate": random.uniform(-5, 15)
    }
    return jsonify(stats)

if __name__ == "__main__":
    app.run(debug=True)