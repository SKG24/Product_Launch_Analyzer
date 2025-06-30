import os
import sys
sys.path.insert(0, 'src')

def test_api_connection():
    """Test Twitter API connection"""
    print("  Testing Twitter API Connection")
    print("=" * 40)
    
    try:
        import tweepy
        
        bearer_token = os.getenv('BEARER_TOKEN')
        if not bearer_token:
            print("  No BEARER_TOKEN found in environment")
            print("  Create .env file with: BEARER_TOKEN=your_token_here")
            return False
        
        print(f"  Bearer token found: {bearer_token[:10]}...{bearer_token[-4:]}")
        
        # Test connection
        client = tweepy.Client(bearer_token=bearer_token)
        
        # Try a simple search
        print("\n  Testing API with simple search...")
        response = client.search_recent_tweets(
            query="iPhone OR Android",
            max_results=10,
            tweet_fields=['created_at', 'public_metrics']
        )
        
        if response.data:
            print(f"  API Test Successful!")
            print(f"   Retrieved {len(response.data)} tweets")
            print(f"   Sample tweet: {response.data[0].text[:50]}...")
            return True
        else:
            print(" ️ API connected but no data returned")
            return False
            
    except tweepy.TooManyRequests:
        print("  Rate limit exceeded - API is working but quota reached")
        return False
    except tweepy.Unauthorized:
        print("  Unauthorized - check your bearer token")
        return False
    except Exception as e:
        print(f"  API Test Failed: {e}")
        return False

if __name__ == "__main__":
    test_api_connection()