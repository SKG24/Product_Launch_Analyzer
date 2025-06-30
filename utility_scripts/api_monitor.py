import logging
import os
import sys
from datetime import datetime

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Configure detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/api_calls.log'),
        logging.StreamHandler()
    ]
)

def check_api_status():
    """Check if Twitter API is configured and working"""
    print("  API Status Check")
    print("=" * 30)
    
    # Check environment variables
    bearer_token = os.getenv('BEARER_TOKEN')
    print(f"Bearer Token: {'  Set' if bearer_token else '  Not Set'}")
    
    if bearer_token:
        print(f"Token preview: {bearer_token[:10]}...{bearer_token[-4:]}")
    
    # Check tweepy availability
    try:
        import tweepy
        print("  tweepy library: Available")
        
        if bearer_token:
            try:
                client = tweepy.Client(bearer_token=bearer_token)
                # Test API call
                me = client.get_me()
                print("  API Connection: Working")
                print(f"  Authenticated as: {me.data.username if me.data else 'Unknown'}")
                return True
            except Exception as e:
                print(f"  API Connection: Failed - {e}")
                return False
        else:
            print("  API Connection: No bearer token")
            return False
            
    except ImportError:
        print("  tweepy library: Not installed")
        return False

def monitor_collection(product, count=10):
    """Monitor a single collection attempt"""
    print(f"\n  Monitoring collection for: {product}")
    print("=" * 40)
    
    # Add current directory to path for imports
    sys.path.insert(0, '.')
    
    try:
        from tweet_collector import collect_tweets
        
        # Collect with monitoring
        tweets = collect_tweets(product, count)
        
        if tweets:
            print(f"  Collection Results:")
            print(f"   Total tweets: {len(tweets)}")
            
            # Analyze tweet sources
            real_api_indicators = 0
            sample_indicators = 0
            
            for tweet in tweets[:3]:  # Check first 3 tweets
                tweet_id = tweet.get('id', '')
                text = tweet.get('text', '')
                
                # Check ID length (real API IDs are longer)
                if len(tweet_id) > 15:
                    real_api_indicators += 1
                else:
                    sample_indicators += 1
                
                print(f"\n   Sample Tweet:")
                print(f"     ID: {tweet_id}")
                print(f"     Text: {text[:60]}...")
                print(f"     Created: {tweet.get('created_at', 'N/A')}")
            
            # Determine source
            if real_api_indicators > sample_indicators:
                print(f"\n  Likely using REAL API data")
                logging.info("Collection appears to be using real API data")
            else:
                print(f"\n ️ Likely using SAMPLE data")
                logging.info("Collection appears to be using sample/fallback data")
        else:
            print("  No tweets collected")
            logging.error("No tweets collected")
            
    except Exception as e:
        print(f"  Monitoring error: {e}")
        logging.error(f"Monitoring error: {e}")

def main():
    print("  Twitter API Monitor")
    print("=" * 40)
    
    # Check API status first
    api_working = check_api_status()
    
    # Ask if user wants to monitor collection
    print("\n" + "=" * 30)
    response = input("Monitor a collection attempt? (y/n): ").strip().lower()
    
    if response == 'y':
        product = input("Enter product name (or press Enter for 'iPhone 15'): ").strip() or "iPhone 15"
        monitor_collection(product)
    
    # Summary
    print(f"\n  Summary")
    print("=" * 20)
    if api_working:
        print("  API is configured and working")
        print("  Your collections should use real Twitter data")
    else:
        print(" ️ API not working or not configured")
        print("  Your collections will use sample data")
        print("\n  To fix:")
        print("1. Get Bearer Token from https://developer.twitter.com/")
        print("2. Create .env file: echo 'BEARER_TOKEN=your_token' > .env")

if __name__ == "__main__":
    main()