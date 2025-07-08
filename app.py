import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import praw
from datetime import datetime

load_dotenv()

app = Flask(__name__)

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/suggest_subreddits")
def suggest_subreddits():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify([])

    try:
        results = reddit.subreddits.search(query, limit=8)
        suggestions = [sub.display_name for sub in results]
        return jsonify(suggestions)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/analyze/<subreddit>")
def analyze(subreddit):
    try:
        subreddit_obj = reddit.subreddit(subreddit)
        posts = []
        for post in subreddit_obj.hot(limit=10):
            posts.append({
                "title": post.title,
                "score": post.score,
                "comments": post.num_comments,
                "timestamp": datetime.utcfromtimestamp(post.created_utc).strftime("%Y-%m-%d %H:%M:%S"),
                "url": post.url,
            })

        # Dummy sentiment values, gerçek analiz eklenebilir
        positive = 40
        neutral = 35
        negative = 25

        response = {
            "sentiments": {
                "positive": positive,
                "neutral": neutral,
                "negative": negative
            },
            "summary": f"Analysis of r/{subreddit} shows {positive}% positive sentiment.",
            "total_posts": len(posts),
            "active_users": "N/A",
            "sample_posts": posts,
            "trending_keywords": [],
            "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": f"Failed to analyze subreddit '{subreddit}': {str(e)}"}), 400


if __name__ == "__main__":
    app.run(debug=True)
