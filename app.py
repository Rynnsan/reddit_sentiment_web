from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Örnek subreddit listesi (gerçek projede Reddit API veya DB’den çekilir)
SUBREDDIT_LIST = [
    "AskReddit", "america", "AmericanCars", "AmateurPhotography",
    "aww", "android", "anime", "Art", "AskScience"
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/suggest_subreddits")
def suggest_subreddits():
    query = request.args.get("q", "").lower()
    suggestions = [sub for sub in SUBREDDIT_LIST if query in sub.lower()]
    return jsonify(suggestions)

@app.route("/analyze/<subreddit>")
def analyze(subreddit):
    # Burada gerçek analiz kodu gelecek
    # Şimdilik dummy örnek:
    dummy_response = {
        "sentiments": {"positive": 30, "neutral": 50, "negative": 20},
        "summary": f"Sample summary for subreddit: r/{subreddit}"
    }
    return jsonify(dummy_response)

if __name__ == "__main__":
    app.run(debug=True)
