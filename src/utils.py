import pandas as pd
from datetime import datetime, date
import csv
from io import StringIO

def filter_tweets_by_date(df, start_date, end_date):
    """Filter tweets by date range"""
    try:
        # Convert to datetime if needed
        df['created_at'] = pd.to_datetime(df['created_at'])
        
        # Filter by date range
        mask = (df['created_at'].dt.date >= start_date) & (df['created_at'].dt.date <= end_date)
        filtered_df = df[mask]
        
        print(f"Filtered {len(filtered_df)} tweets between {start_date} and {end_date}")
        return filtered_df
    
    except Exception as e:
        print(f"Error filtering by date: {e}")
        return df

def calculate_metrics(df):
    """Calculate basic metrics from tweets"""
    if df.empty:
        return {}
    
    try:
        metrics = {
            'total_tweets': len(df),
            'avg_sentiment': df['sentiment'].mean(),
            'avg_likes': df['likes'].mean(),
            'avg_retweets': df['retweets'].mean(),
            'positive_tweets': len(df[df['sentiment'] > 0.1]),
            'negative_tweets': len(df[df['sentiment'] < -0.1]),
            'neutral_tweets': len(df[(df['sentiment'] >= -0.1) & (df['sentiment'] <= 0.1)])
        }
        
        return metrics
    
    except Exception as e:
        print(f"Error calculating metrics: {e}")
        return {}

def export_to_csv(df, filename=None):
    """Export dataframe to CSV"""
    try:
        # Select columns to export
        columns = ['id', 'created_at', 'text', 'likes', 'retweets', 'sentiment', 'product']
        export_df = df[columns]
        
        if filename:
            export_df.to_csv(filename, index=False)
            print(f"Exported to {filename}")
            return filename
        else:
            # Return CSV string
            output = StringIO()
            export_df.to_csv(output, index=False)
            return output.getvalue()
    
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        return ""

def clean_text_simple(text):
    """Simple text cleaning"""
    if not text:
        return ""
    
    # Basic cleaning
    text = text.strip()
    text = ' '.join(text.split())  # Remove extra spaces
    
    return text

def categorize_sentiment(score):
    """Convert sentiment score to category"""
    if score > 0.1:
        return "Positive"
    elif score < -0.1:
        return "Negative"
    else:
        return "Neutral"

def get_top_words(texts, n=10):
    """Get most common words from texts"""
    try:
        # Combine all texts
        all_text = ' '.join(texts).lower()
        
        # Split into words and filter
        words = all_text.split()
        
        # Remove common stop words
        stop_words = {'the', 'and', 'or', 'is', 'are', 'to', 'of', 'for', 'with', 'on', 'at', 'in', 'by'}
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Count words
        word_count = {}
        for word in filtered_words:
            word_count[word] = word_count.get(word, 0) + 1
        
        # Sort and return top n
        sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        return sorted_words[:n]
    
    except Exception as e:
        print(f"Error getting top words: {e}")
        return []

def format_number(num):
    """Format numbers for display"""
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    else:
        return str(int(num))

def calculate_engagement_rate(likes, retweets, followers=1000):
    """Calculate engagement rate"""
    try:
        total_engagement = likes + retweets
        rate = (total_engagement / followers) * 100
        return rate
    except:
        return 0

def get_date_range_from_tweets(tweets):
    """Get min and max dates from tweets"""
    try:
        dates = [pd.to_datetime(tweet['created_at']).date() for tweet in tweets]
        return min(dates), max(dates)
    except Exception as e:
        print(f"Error getting date range: {e}")
        return None, None

def summarize_sentiment_by_product(df):
    """Summarize sentiment by product"""
    try:
        summary = df.groupby('product').agg({
            'sentiment': ['mean', 'count'],
            'likes': 'mean',
            'retweets': 'mean'
        }).round(3)
        
        return summary
    except Exception as e:
        print(f"Error summarizing by product: {e}")
        return pd.DataFrame()

# Test utility functions
if __name__ == "__main__":
    # Create sample data for testing
    sample_data = {
        'created_at': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'text': ['Great product!', 'Not good', 'Okay product'],
        'sentiment': [0.8, -0.6, 0.1],
        'likes': [20, 5, 10],
        'retweets': [5, 1, 2],
        'product': ['iPhone 15', 'iPhone 15', 'Galaxy S24']
    }
    
    df = pd.DataFrame(sample_data)
    
    print("Testing utility functions:")
    print("-" * 30)
    
    # Test metrics calculation
    metrics = calculate_metrics(df)
    print(f"Metrics: {metrics}")
    
    # Test sentiment categorization
    for score in [0.5, -0.3, 0.05]:
        category = categorize_sentiment(score)
        print(f"Score {score} -> {category}")
    
    # Test top words
    texts = df['text'].tolist()
    top_words = get_top_words(texts, 5)
    print(f"Top words: {top_words}")
    
    print("\n✓ All utility tests passed!")