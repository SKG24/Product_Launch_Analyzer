import os
import random
import pandas as pd
from datetime import datetime, timedelta

# Try to import tweepy for Twitter API
try:
    import tweepy
    TWEEPY_AVAILABLE = True
except ImportError:
    TWEEPY_AVAILABLE = False
    print("tweepy not installed. Using sample data only.")

def get_twitter_client():
    """Get Twitter API client if available"""
    bearer_token = os.getenv('BEARER_TOKEN')
    
    if not bearer_token or not TWEEPY_AVAILABLE:
        return None
    
    try:
        client = tweepy.Client(bearer_token=bearer_token)
        return client
    except Exception as e:
        print(f"Error creating Twitter client: {e}")
        return None

def collect_tweets_api(query, count=50):
    """Collect tweets using Twitter API"""
    client = get_twitter_client()
    
    if not client:
        return []
    
    try:
        # Search for recent tweets
        tweets = client.search_recent_tweets(
            query=query,
            max_results=min(count, 100),  # API limit
            tweet_fields=['created_at', 'public_metrics', 'author_id']
        )
        
        if not tweets.data:
            return []
        
        # Convert to our format
        result = []
        for tweet in tweets.data:
            metrics = tweet.public_metrics or {}
            
            tweet_data = {
                'id': str(tweet.id),
                'created_at': str(tweet.created_at),
                'text': tweet.text,
                'user_id': str(tweet.author_id),
                'likes': metrics.get('like_count', 0),
                'retweets': metrics.get('retweet_count', 0)
            }
            
            result.append(tweet_data)
        
        print(f"Collected {len(result)} tweets from API")
        return result
    
    except Exception as e:
        print(f"Error collecting from API: {e}")
        return []

def generate_sample_tweets(product, count=50):
    """Generate sample tweets for testing"""
    
    # Sample tweet templates
    templates = {
        'positive': [
            f"Love the new {product}! Amazing features  ",
            f"{product} is incredible! Best upgrade ever  ",
            f"Just got my {product} and it's perfect!  ",
            f"{product} exceeded my expectations! Highly recommend  ",
            f"Outstanding quality! {product} is worth every penny  "
        ],
        'negative': [
            f"{product} is disappointing. Not worth the price  ",
            f"Had high hopes for {product} but it's mediocre  ",
            f"{product} has too many issues. Returning it  ",
            f"Not impressed with {product}. Expected better  ",
            f"{product} is overpriced for what you get  "
        ],
        'neutral': [
            f"Just unboxed my {product}. First impressions...",
            f"Testing out the {product} features today",
            f"{product} arrived. Setting it up now",
            f"Comparing {product} with my old device",
            f"{product} review coming soon. Stay tuned"
        ]
    }
    
    tweets = []
    base_date = datetime.now() - timedelta(days=30)
    
    for i in range(count):
        # Random sentiment type
        sentiment_type = random.choice(['positive', 'negative', 'neutral'])
        tweet_text = random.choice(templates[sentiment_type])
        
        # Random date within last 30 days
        random_days = random.randint(0, 29)
        random_hours = random.randint(0, 23)
        tweet_date = base_date + timedelta(days=random_days, hours=random_hours)
        
        # Random engagement
        if sentiment_type == 'positive':
            likes = random.randint(10, 100)
            retweets = random.randint(2, 20)
        elif sentiment_type == 'negative':
            likes = random.randint(0, 30)
            retweets = random.randint(0, 8)
        else:  # neutral
            likes = random.randint(5, 50)
            retweets = random.randint(1, 10)
        
        tweet = {
            'id': str(random.randint(1000000000, 9999999999)),
            'created_at': tweet_date.strftime('%Y-%m-%d %H:%M:%S'),
            'text': tweet_text,
            'user_id': f'user_{random.randint(1000, 9999)}',
            'likes': likes,
            'retweets': retweets
        }
        
        tweets.append(tweet)
    
    print(f"Generated {len(tweets)} sample tweets for {product}")
    return tweets

def collect_tweets(query, count=50):
    """Main function to collect tweets"""
    print(f"Collecting tweets for: {query}")
    
    # Try API first
    tweets = collect_tweets_api(query, count)
    
    # If API fails, use sample data
    if not tweets:
        print("Using sample data instead of API")
        tweets = generate_sample_tweets(query, count)
    
    return tweets

def save_tweets_to_csv(tweets, filename):
    """Save tweets to CSV file"""
    if not tweets:
        print("No tweets to save")
        return
    
    try:
        df = pd.DataFrame(tweets)
        df.to_csv(filename, index=False)
        print(f"Saved {len(tweets)} tweets to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def load_tweets_from_csv(filename):
    """Load tweets from CSV file"""
    try:
        df = pd.read_csv(filename)
        return df.to_dict('records')
    except Exception as e:
        print(f"Error loading from CSV: {e}")
        return []


def collect_tweets_with_monitoring(query, count=50):
    """Collect tweets with detailed monitoring"""
    import logging
    logger = logging.getLogger(__name__)
    
    print(f"\n  MONITORING: Collecting tweets for '{query}'")
    print("=" * 50)
    
    # Check API availability
    client = get_twitter_client()
    if client:
        print("  Twitter API client available")
        logger.info(f"API client initialized for query: {query}")
        
        try:
            # Try API collection
            print("  Attempting API collection...")
            tweets = collect_tweets_api(query, count)
            
            if tweets:
                print(f"  API SUCCESS: Collected {len(tweets)} real tweets")
                logger.info(f"API collection successful: {len(tweets)} tweets")
                
                # Log sample tweet for verification
                if tweets:
                    sample_tweet = tweets[0]
                    logger.info(f"Sample API tweet ID: {sample_tweet['id']}")
                    print(f"   Sample tweet ID: {sample_tweet['id']}")
                    print(f"   Sample text: {sample_tweet['text'][:60]}...")
                
                return tweets
            else:
                print(" ️ API returned no results, falling back to sample data")
                logger.warning("API returned no results")
                
        except Exception as e:
            print(f"  API ERROR: {e}")
            logger.error(f"API error: {e}")
    else:
        print("  No API client available")
        logger.warning("No API client available")
    
    # Fallback to sample data
    print("  Using sample data generation...")
    logger.info("Using fallback sample data")
    tweets = generate_sample_tweets(query, count)
    
    if tweets:
        print(f"  FALLBACK SUCCESS: Generated {len(tweets)} sample tweets")
        sample_tweet = tweets[0]
        print(f"   Sample tweet ID: {sample_tweet['id']}")
        print(f"   Sample text: {sample_tweet['text'][:60]}...")
    
    return tweets


# Test the collector
if __name__ == "__main__":
    # Test products
    products = ["iPhone 15", "Galaxy S24", "Pixel 8"]
    
    for product in products:
        print(f"\nTesting collection for {product}")
        tweets = collect_tweets(product, count=10)
        
        if tweets:
            print(f"Sample tweet: {tweets[0]['text']}")
            print(f"Engagement: {tweets[0]['likes']} likes, {tweets[0]['retweets']} retweets")
        
        print("-" * 50)