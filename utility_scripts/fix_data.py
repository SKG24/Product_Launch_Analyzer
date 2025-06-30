import os
import sys

# Add src to path
sys.path.insert(0, 'src')

def main():
    print("  Quick Fix - Product Launch Analyzer")
    print("=" * 40)
    
    # Step 1: Ensure directories exist
    print("1. Creating directories...")
    os.makedirs('data', exist_ok=True)
    os.makedirs('src', exist_ok=True)
    print("  Directories ready")
    
    # Step 2: Initialize database
    print("\n2. Initializing database...")
    try:
        from database import create_table, DATABASE_PATH
        create_table()
        print(f"  Database ready: {DATABASE_PATH}")
    except Exception as e:
        print(f"  Database error: {e}")
        return
    
    # Step 3: Run quick pipeline test
    print("\n3. Running quick data collection...")
    try:
        from pipeline import run_pipeline_for_product
        success = run_pipeline_for_product("iPhone 15", tweet_count=10)
        
        if success:
            print("  Data collection successful")
        else:
            print("  Data collection failed")
            return
    except Exception as e:
        print(f"  Pipeline error: {e}")
        return
    
    # Step 4: Verify data
    print("\n4. Verifying data...")
    try:
        from database import count_tweets, get_products
        tweet_count = count_tweets()
        products = get_products()
        
        print(f"  Found {tweet_count} tweets")
        print(f"  Products: {products}")
        
    except Exception as e:
        print(f"  Verification error: {e}")
        return
    
    print("\n  Fix complete! Now you can run:")
    print("streamlit run src/app.py")

if __name__ == "__main__":
    main()