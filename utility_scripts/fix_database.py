import sys
import os

# Add src to path
sys.path.insert(0, 'src')

def fix_database_schema():
    """Fix the database schema issue"""
    print("  Fixing Database Schema")
    print("=" * 30)
    
    try:
        from database import create_table, count_tweets, get_products
        
        # Show current status
        try:
            tweet_count = count_tweets()
            products = get_products()
            print(f"Current data: {tweet_count} tweets, products: {products}")
        except Exception as e:
            print(f"Current status: {e}")
        
        # Fix the schema
        print("\nFixing database schema...")
        create_table()
        print("  Database schema fixed!")
        
        # Verify the fix
        tweet_count = count_tweets()
        print(f"  Database working: {tweet_count} tweets found")
        
        return True
        
    except Exception as e:
        print(f"  Error fixing database: {e}")
        return False

def run_quick_test():
    """Run a quick test after fixing"""
    print("\n  Running Quick Test")
    print("=" * 30)
    
    try:
        from pipeline import run_pipeline_for_product
        
        print("Testing with one product...")
        success = run_pipeline_for_product("iPhone 15", tweet_count=5)
        
        if success:
            print("  Test successful - database is working!")
            
            # Show final status
            from database import count_tweets, get_products
            tweet_count = count_tweets()
            products = get_products()
            print(f"Final status: {tweet_count} tweets, products: {products}")
            
        else:
            print("  Test failed")
            
    except Exception as e:
        print(f"  Test error: {e}")

def main():
    print(" ️ Database Schema Fixer")
    print("=" * 40)
    print("This will fix the 'user_id column' error.")
    print()
    
    # Fix the schema
    if fix_database_schema():
        # Ask if user wants to run test
        response = input("\nRun quick test? (y/n): ").strip().lower()
        if response == 'y':
            run_quick_test()
        
        print("\n  Ready to use!")
        print("Now run: streamlit run src/app.py")
    else:
        print("\n  Fix failed. You may need to delete the database file and start fresh.")
        print("To start fresh: rm data/tweets.db && python fix_data.py")

if __name__ == "__main__":
    main()