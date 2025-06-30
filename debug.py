import os
import sys

# Add src to path
sys.path.insert(0, 'src')

def check_database():
    """Check database status"""
    print("  Database Diagnostic")
    print("=" * 30)
    
    try:
        from database import DATABASE_PATH, count_tweets, get_products
        
        print(f"Database path: {DATABASE_PATH}")
        print(f"Database exists: {os.path.exists(DATABASE_PATH)}")
        
        if os.path.exists(DATABASE_PATH):
            print(f"Database size: {os.path.getsize(DATABASE_PATH)} bytes")
            
            # Check contents
            tweet_count = count_tweets()
            print(f"Total tweets: {tweet_count}")
            
            products = get_products()
            print(f"Products: {products}")
            
            if tweet_count > 0:
                print("  Database has data!")
            else:
                print("  Database is empty")
        else:
            print("  Database file not found")
            
    except Exception as e:
        print(f"  Error: {e}")

def check_project_structure():
    """Check project directory structure"""
    print("\n  Project Structure")
    print("=" * 30)
    
    files_to_check = [
        'src/app.py',
        'src/database.py', 
        'src/pipeline.py',
        'data',
        'data/tweets.db'
    ]
    
    for file_path in files_to_check:
        exists = os.path.exists(file_path)
        status = " " if exists else " "
        print(f"{status} {file_path}")

def run_quick_test():
    """Run a quick pipeline test"""
    print("\n  Quick Pipeline Test")
    print("=" * 30)
    
    try:
        sys.path.insert(0, 'src')
        from pipeline import run_pipeline_for_product
        
        print("Running pipeline for test product...")
        success = run_pipeline_for_product("Test Product", tweet_count=5)
        
        if success:
            print("  Pipeline test successful")
            # Check database again
            check_database()
        else:
            print("  Pipeline test failed")
            
    except Exception as e:
        print(f"  Pipeline test error: {e}")

def main():
    print("  Product Launch Analyzer - Diagnostics")
    print("=" * 50)
    
    # Check project structure
    check_project_structure()
    
    # Check database
    check_database()
    
    # Ask if user wants to run test
    print("\n" + "=" * 30)
    response = input("Run quick pipeline test? (y/n): ").strip().lower()
    
    if response == 'y':
        run_quick_test()
    
    print("\n  Diagnostic complete!")

if __name__ == "__main__":
    main()