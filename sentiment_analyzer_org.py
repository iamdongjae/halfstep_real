import sys
from textblob import TextBlob

def analyze_sentiment(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity

    if sentiment_score > 0:
        return 'positive'
    elif sentiment_score == 0:
        return 'neutral'
    else:
        return 'negative'

if __name__ == "__main__":
    file_path = sys.argv[1]
    sentiment = analyze_sentiment(file_path)
    print(sentiment)
