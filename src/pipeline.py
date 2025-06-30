import time
from datetime import datetime

# Import our modules
from tweet_collector import collect_tweets
from sentiment_analyzer import analyze_tweets_sentiment
from database import create_table, insert_tweets

def run_pipeline_for_product(product_name, tweet_count=50):
    """Run pipeline for a single product"""
    print(f"\n{'='*50}")
    print(f"Processing: {product_name}")
    print(f"{'='*50}")
    
    try:
        # Step 1: Collect tweets
        print("1. Collecting tweets...")
        tweets = collect_tweets(product_name, tweet_count)
        
        if not tweets:
            print(f"  No tweets collected for {product_name}")
            return False
        
        print(f"  Collected {len(tweets)} tweets")
        
        # Step 2: Analyze sentiment
        print("2. Analyzing sentiment...")
        tweets_with_sentiment = analyze_tweets_sentiment(tweets)
        print("  Sentiment analysis complete")
        
        # Step 3: Add product name
        for tweet in tweets_with_sentiment:
            tweet['product'] = product_name
        
        # Step 4: Save to database
        print("3. Saving to database...")
        insert_tweets(tweets_with_sentiment)
        print("  Data saved successfully")
        
        # Show sample results
        print("\n  Sample Results:")
        for i, tweet in enumerate(tweets_with_sentiment[:3]):
            sentiment = tweet['sentiment']
            sentiment_label = tweet['sentiment_label']
            print(f"{i+1}. Sentiment: {sentiment:.3f} ({sentiment_label})")
            print(f"   Text: {tweet['text'][:60]}...")
        
        return True
    
    except Exception as e:
        print(f"  Error processing {product_name}: {e}")
        return False

def run_full_pipeline(products=None, tweets_per_product=50, delay_seconds=10):
    """Run pipeline for multiple products"""
    
    # Default products if none provided
    if products is None:
        products = [
            "iPhone 15",
            "Galaxy S24", 
            "Pixel 8",
            "OnePlus 12",
            "Nothing Phone"
        ]
    
    print(f"  Starting pipeline for {len(products)} products")
    print(f"  Configuration:")
    print(f"   - Tweets per product: {tweets_per_product}")
    print(f"   - Delay between products: {delay_seconds} seconds")
    
    # Initialize database
    create_table()
    
    # Process each product
    successful = 0
    failed = 0
    
    for i, product in enumerate(products):
        success = run_pipeline_for_product(product, tweets_per_product)
        
        if success:
            successful += 1
        else:
            failed += 1
        
        # Add delay between products (except for the last one)
        if i < len(products) - 1:
            print(f"\n  Waiting {delay_seconds} seconds before next product...")
            time.sleep(delay_seconds)
    
    # Final summary
    print(f"\n  Pipeline Complete!")
    print(f"{'='*50}")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Total products processed: {len(products)}")
    print(f" ️  Pipeline finished at: {datetime.now().strftime('%H:%M:%S')}")

def quick_test():
    """Quick test with sample data"""
    print("  Running quick test...")
    
    # Test with one product and fewer tweets
    success = run_pipeline_for_product("iPhone 15", tweet_count=10)
    
    if success:
        print("  Quick test passed!")
    else:
        print("  Quick test failed!")

# Main execution
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Run quick test
        quick_test()
    elif len(sys.argv) > 1 and sys.argv[1] == "single":
        # Run for single product
        product = sys.argv[2] if len(sys.argv) > 2 else "iPhone 15"
        run_pipeline_for_product(product)
    else:
        # Run full pipeline
        run_full_pipeline()