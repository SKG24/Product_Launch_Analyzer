import sys
import os

# Add src to path
sys.path.insert(0, 'src')

def collect_all_products():
    """Collect data for all products"""
    print("  Collecting Data for All Products")
    print("=" * 40)
    
    # List of products to analyze
    products = [
        "iPhone 15",
        "Galaxy S24", 
        "Pixel 8",
        "OnePlus 12",
        "Nothing Phone"
    ]
    
    try:
        from database import create_table
        from pipeline import run_pipeline_for_product
        
        # Fix database schema first
        print("Setting up database...")
        create_table()
        print("  Database ready")
        
        # Collect data for each product
        successful = 0
        
        for i, product in enumerate(products, 1):
            print(f"\n[{i}/{len(products)}] Collecting data for: {product}")
            try:
                success = run_pipeline_for_product(product, tweet_count=30)
                if success:
                    successful += 1
                    print(f"  {product} complete")
                else:
                    print(f"  {product} failed")
            except Exception as e:
                print(f"  Error with {product}: {e}")
        
        # Show final results
        print(f"\n  Data collection complete!")
        print(f"  Successfully processed: {successful}/{len(products)} products")
        
        # Show what's in database
        from database import count_tweets, get_products
        total_tweets = count_tweets()
        available_products = get_products()
        
        print(f"  Database now contains:")
        print(f"   - {total_tweets} total tweets")
        print(f"   - {len(available_products)} products: {available_products}")
        
        if len(available_products) > 1:
            print(f"\n  Ready! Now you'll see {len(available_products)} products in the filter")
            print("Run: streamlit run src/app.py")
        else:
            print(f"\n ️  Only {len(available_products)} product in database")
            
    except Exception as e:
        print(f"  Error: {e}")

def quick_test():
    """Quick test with 2 products"""
    print("  Quick Test - 2 Products")
    print("=" * 30)
    
    products = ["iPhone 15", "Galaxy S24"]
    
    try:
        from database import create_table
        from pipeline import run_pipeline_for_product
        
        create_table()
        
        for product in products:
            print(f"Collecting {product}...")
            run_pipeline_for_product(product, tweet_count=15)
        
        from database import get_products
        available_products = get_products()
        print(f"  Products in database: {available_products}")
        
    except Exception as e:
        print(f"  Error: {e}")

def main():
    print("  Product Data Collector")
    print("=" * 40)
    print("1. Collect all 5 products (full dataset)")
    print("2. Quick test with 2 products")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        collect_all_products()
    elif choice == '2':
        quick_test()
    elif choice == '3':
        print("Goodbye!")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()