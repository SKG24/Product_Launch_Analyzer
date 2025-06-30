import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def run_pipeline():
    """Run the data collection pipeline"""
    try:
        from pipeline import run_full_pipeline
        print("  Starting data collection pipeline...")
        print("This will collect data for iPhone 15, Galaxy S24, Pixel 8, OnePlus 12, and Nothing Phone")
        run_full_pipeline()
    except ImportError as e:
        print(f"  Import error: {e}")
        print("Make sure you're in the project root directory")
    except Exception as e:
        print(f"  Error: {e}")

def run_quick_collection():
    """Quick collection for 3 products"""
    try:
        from pipeline import run_pipeline_for_product
        from database import create_table, get_products, count_tweets
        
        print("  Quick collection for 3 products...")
        create_table()
        
        products = ["iPhone 15", "Galaxy S24", "Pixel 8"]
        successful = 0
        
        for i, product in enumerate(products, 1):
            print(f"\n[{i}/{len(products)}] Collecting {product}...")
            success = run_pipeline_for_product(product, tweet_count=25)
            if success:
                successful += 1
        
        # Show results
        available_products = get_products()
        total_tweets = count_tweets()
        print(f"\n  Complete! {total_tweets} tweets for {len(available_products)} products")
        print(f"Products: {available_products}")
        
    except Exception as e:
        print(f"  Error: {e}")

def run_dashboard():
    """Launch the Streamlit dashboard"""
    print("  Launching dashboard...")
    print("Run this command: streamlit run src/app.py")

def run_tests():
    """Run the test suite"""
    try:
        import subprocess
        result = subprocess.run([sys.executable, 'tests/test_basic.py'], 
                              capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
    except Exception as e:
        print(f"  Test error: {e}")

def main():
    print("  Product Launch Analyzer")
    print("=" * 30)
    print("1. Quick collection (3 products)")
    print("2. Full collection (5 products)") 
    print("3. Launch dashboard")
    print("4. Run tests")
    print("5. Exit")
    
    while True:
        try:
            choice = input("\nEnter choice (1-5): ").strip()
            
            if choice == '1':
                run_quick_collection()
                break
            elif choice == '2':
                run_pipeline()
                break
            elif choice == '3':
                run_dashboard()
                break
            elif choice == '4':
                run_tests()
                break
            elif choice == '5':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1-5.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()