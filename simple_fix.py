import sys
import os

# Add src to path
sys.path.insert(0, 'src')

def main():
    print(" Simple Fix - Product Launch Analyzer")
    print("Fixing database and collecting data for multiple products...")
    print("=" * 60)
    
    try:
        # Fix database schema
        from database import create_table
        create_table()
        print(" Database schema fixed")
        
        # Collect data for multiple products
        products = ["iPhone 15", "Galaxy S24", "Pixel 8"]
        
        from pipeline import run_pipeline_for_product
        successful = 0
        
        for i, product in enumerate(products, 1):
            print(f"\n[{i}/{len(products)}] Collecting data for: {product}")
            success = run_pipeline_for_product(product, tweet_count=25)
            if success:
                successful += 1
        
        print(f"\n Fix complete!")
        print(f" Successfully collected data for {successful}/{len(products)} products")
        
        # Show what's available
        from database import get_products, count_tweets
        available_products = get_products()
        total_tweets = count_tweets()
        
        print(f" Database contains {total_tweets} tweets for products: {available_products}")
        print(f" You'll now see {len(available_products)} products in the dashboard filter!")
        print("\nRun: streamlit run src/app.py")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()