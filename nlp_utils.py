from transformers import pipeline

# Sentiment analysis pipeline (ilk kullanımda model indirilecek)
sentiment_pipeline = pipeline("sentiment-analysis")

def get_sentiment_label(text):
    try:
        result = sentiment_pipeline(text[:512])[0]  # Max 512 karakter
        label = result['label'].lower()  # POSITIVE, NEGATIVE
        if label == 'positive':
            return 'positive'
        elif label == 'negative':
            return 'negative'
        else:
            return 'neutral'
    except Exception as e:
        print("Sentiment error:", e)
        return 'neutral'
