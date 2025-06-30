import os
import sys

def create_directories():
    """Create necessary project directories"""
    directories = [
        'data',
        'logs',
        'src',
        'tests',
        'scripts'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
        else:
            print(f"Directory exists: {directory}")

def setup_database():
    """Initialize the database"""
    # Add src to path
    sys.path.insert(0, 'src')
    
    try:
        from database import create_table
        create_table()
        print(" Database initialized successfully")
    except Exception as e:
        print(f" Database setup failed: {e}")

def install_dependencies():
    """Install required dependencies"""
    print("\n Installing dependencies...")
    print("Run this command:")
    print("pip install streamlit pandas plotly textblob tweepy python-dotenv")

def main():
    print(" Setting up Product Launch Analyzer")
    print("=" * 40)
    
    # Create directories
    print("\n1. Creating directories...")
    create_directories()
    
    # Setup database
    print("\n2. Setting up database...")
    setup_database()
    
    # Show next steps
    print("\n3. Next steps:")
    install_dependencies()
    print("\n Usage:")
    print("  python scripts/run_pipeline.py          # Collect data")
    print("  streamlit run src/app.py                # Launch dashboard")
    
    print("\n Setup complete!")

if __name__ == "__main__":
    main()