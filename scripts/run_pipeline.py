import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pipeline import run_full_pipeline, run_pipeline_for_product, quick_test

def main():
    print("  Product Launch Analyzer - Pipeline Runner")
    print("=" * 50)
    
    if len(sys.argv) == 1:
        # No arguments - run full pipeline
        print("Running full pipeline for all products...")
        run_full_pipeline()
    
    elif sys.argv[1] == "test":
        # Quick test
        print("Running quick test...")
        quick_test()
    
    elif sys.argv[1] == "single":
        # Single product
        if len(sys.argv) > 2:
            product = sys.argv[2]
        else:
            product = input("Enter product name: ")
        
        print(f"Running pipeline for: {product}")
        run_pipeline_for_product(product)
    
    elif sys.argv[1] == "help":
        # Show help
        print_help()
    
    else:
        print(f"Unknown command: {sys.argv[1]}")
        print("Use 'python run_pipeline.py help' for usage information")

def print_help():
    """Print usage help"""
    print("Usage:")
    print("  python run_pipeline.py              # Run full pipeline")
    print("  python run_pipeline.py test         # Quick test")
    print("  python run_pipeline.py single       # Single product (interactive)")
    print("  python run_pipeline.py single 'iPhone 15'  # Single product")
    print("  python run_pipeline.py help         # Show this help")
    print()
    print("Examples:")
    print("  python run_pipeline.py")
    print("  python run_pipeline.py test")
    print("  python run_pipeline.py single 'Galaxy S24'")

if __name__ == "__main__":
    main()