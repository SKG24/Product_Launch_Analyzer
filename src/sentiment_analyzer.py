import re
from textblob import TextBlob

def clean_text(text):
    """Clean text for sentiment analysis"""
    if not text:
        return ""
    
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    
    # Remove mentions and hashtags
    text = re.sub(r'@\w+|#\w+', '', text)
    
    # Remove extra spaces
    text = ' '.join(text.split())
    
    return text.strip()

def analyze_sentiment(text):
    """Analyze sentiment of text using TextBlob"""
    try:
        # Clean the text
        cleaned_text = clean_text(text)
        
        if not cleaned_text:
            return 0.0
        
        # Get sentiment polarity (-1 to 1)
        blob = TextBlob(cleaned_text)
        polarity = blob.sentiment.polarity
        
        return polarity
    
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return 0.0

def get_sentiment_label(score):
    """Convert sentiment score to label"""
    if score > 0.1:
        return "Positive"
    elif score < -0.1:
        return "Negative"
    else:
        return "Neutral"

def analyze_tweets_sentiment(tweets):
    """Add sentiment analysis to list of tweets"""
    for tweet in tweets:
        text = tweet.get('text', '')
        
        # Calculate sentiment
        sentiment_score = analyze_sentiment(text)
        sentiment_label = get_sentiment_label(sentiment_score)
        
        # Add to tweet
        tweet['sentiment'] = sentiment_score
        tweet['sentiment_label'] = sentiment_label
    
    return tweets

def batch_sentiment_analysis(texts):
    """Analyze sentiment for multiple texts"""
    results = []
    
    for text in texts:
        score = analyze_sentiment(text)
        label = get_sentiment_label(score)
        
        results.append({
            'text': text,
            'sentiment_score': score,
            'sentiment_label': label
        })
    
    return results

# Test the sentiment analyzer
if __name__ == "__main__":
    test_texts = [
        "I love this new iPhone! It's amazing!",
        "This product is terrible, waste of money.",
        "The phone is okay, nothing special.",
        "Best purchase ever! Highly recommend!",
        "Poor quality, very disappointed."
    ]
    
    print("Testing Sentiment Analysis:")
    print("-" * 40)
    
    for text in test_texts:
        score = analyze_sentiment(text)
        label = get_sentiment_label(score)
        
        print(f"Text: {text}")
        print(f"Score: {score:.3f} | Label: {label}")
        print()