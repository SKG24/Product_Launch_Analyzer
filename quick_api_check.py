import os
import sys

# Add src to path
sys.path.insert(0, 'src')

def check_api_status():
    """Quick check of API status"""
    print("  Quick API Status Check")
    print("=" * 30)
    
    # Check environment
    bearer_token = os.getenv('BEARER_TOKEN')
    print(f"1. Bearer Token: {'  Found' if bearer_token else '  Missing'}")
    
    # Check tweepy
    try:
        import tweepy
        print("2. Tweepy Library:   Installed")
    except ImportError:
        print("2. Tweepy Library:   Not installed")
        print("   Run: pip install tweepy")
        return False
    
    # Test API if token exists
    if bearer_token:
        try:
            client = tweepy.Client(bearer_token=bearer_token)
            # Quick test
            response = client.search_recent_tweets(query="test", max_results=10)
            print("3. API Connection:   Working")
            print(f"4. Test Search:   Found {len(response.data) if response.data else 0} tweets")
            return True
        except tweepy.TooManyRequests:
            print("3. API Connection:  ️ Rate Limited (but working)")
            return False
        except tweepy.Unauthorized:
            print("3. API Connection:   Invalid Token")
            return False
        except Exception as e:
            print(f"3. API Connection:   Error - {e}")
            return False
    else:
        print("3. API Connection:   No token to test")
        return False

def test_collection():
    """Test actual tweet collection"""
    print("\n  Testing Tweet Collection")
    print("=" * 30)
    
    try:
        from tweet_collector import collect_tweets
        
        # Test with small query
        print("Testing collection for 'iPhone'...")
        tweets = collect_tweets("iPhone", count=5)
        
        if tweets:
            print(f"  Collected {len(tweets)} tweets")
            
            # Check first tweet to determine source
            first_tweet = tweets[0]
            tweet_id = first_tweet.get('id', '')
            text = first_tweet.get('text', '')
            
            print(f"\nSample Tweet:")
            print(f"  ID: {tweet_id}")
            print(f"  Text: {text[:50]}...")
            
            # Determine if real or sample
            if len(tweet_id) > 15 and not any(template in text for template in ["Love the new", "Amazing features", "Outstanding quality"]):
                print("  Status: Likely REAL API data")
            else:
                print("  Status: Likely SAMPLE data")
        else:
            print("  No tweets collected")
            
    except Exception as e:
        print(f"  Collection test failed: {e}")

def main():
    print("  Twitter API Quick Check")
    print("=" * 40)
    
    # Check API status
    api_working = check_api_status()
    
    # Test collection
    test_collection()
    
    # Summary
    print("\n  Summary")
    print("=" * 20)
    if api_working:
        print("  Your system should be using REAL Twitter data")
        print("  Real tweets have long IDs and varied content")
    else:
        print(" ️ Your system is using SAMPLE data")
        print("  Sample tweets have short IDs and template-like content")
    
    print("\n  To enable real API data:")
    print("1. Get Twitter Bearer Token from https://developer.twitter.com/")
    print("2. Create .env file: echo 'BEARER_TOKEN=your_token' > .env")
    print("3. Run this check again")

if __name__ == "__main__":
    main()