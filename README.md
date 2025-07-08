# 📊 Reddit Sentiment Web

Welcome to **Reddit Sentiment Web** — a sleek, full-stack web app that analyzes the emotional tone of Reddit discussions in real time. Whether you're tracking market sentiment, social trends, or just curious about what Reddit thinks, this tool gives you a visual pulse of the hive mind.

---

## 🚀 Features

- 🔍 **Live Sentiment Analysis**: Fetches Reddit posts and comments, then classifies them as Positive, Negative, or Neutral.
- 🌐 **Interactive Web Interface**: Clean, responsive UI built with HTML, CSS, and JavaScript.
- 🧠 **Python-Powered Backend**: Flask app handles routing, API calls, and sentiment logic.
- 📈 **Data Visualization Ready**: Easily extendable with charts or dashboards.

---

## 🛠️ Tech Stack

| Layer       | Tech Used             |
|-------------|------------------------|
| Backend     | Python, Flask          |
| Frontend    | HTML, CSS, JavaScript  |
| Sentiment   | (Pluggable NLP model)  |
| Deployment  | (Coming soon 🚧)       |

---

## 📦 Getting Started

```bash
# Clone the repo
git clone https://github.com/Rynnsan/reddit_sentiment_web.git
cd reddit_sentiment_web

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\\Scripts\\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
