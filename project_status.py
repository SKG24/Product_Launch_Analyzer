import os
import sys

def check_project_structure():
    """Check if all necessary files and directories exist"""
    print("  Project Structure Check")
    print("=" * 30)
    
    required_items = [
        ('src/', 'directory'),
        ('src/app.py', 'file'),
        ('src/database.py', 'file'),
        ('src/pipeline.py', 'file'),
        ('src/tweet_collector.py', 'file'),
        ('data/', 'directory'),
        ('tests/', 'directory'),
        ('requirements.txt', 'file')
    ]
    
    all_good = True
    
    for item, item_type in required_items:
        if item_type == 'directory':
            exists = os.path.isdir(item)
        else:
            exists = os.path.isfile(item)
        
        status = " " if exists else " "
        print(f"{status} {item}")
        
        if not exists:
            all_good = False
    
    return all_good

def check_dependencies():
    """Check if required packages are installed"""
    print("\n  Dependencies Check")
    print("=" * 30)
    
    required_packages = [
        'streamlit',
        'pandas', 
        'plotly',
        'textblob',
        'tweepy',
        'python-dotenv'
    ]
    
    all_installed = True
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"  {package}")
        except ImportError:
            print(f"  {package}")
            all_installed = False
    
    return all_installed

def check_database_status():
    """Check database status"""
    print("\n ️ Database Status")
    print("=" * 30)
    
    db_path = "data/tweets.db"
    
    if os.path.exists(db_path):
        print(f"  Database exists: {db_path}")
        print(f"   Size: {os.path.getsize(db_path)} bytes")
        
        # Try to get data
        try:
            sys.path.insert(0, 'src')
            from database import count_tweets, get_products
            
            tweet_count = count_tweets()
            products = get_products()
            
            print(f"   Tweets: {tweet_count}")
            print(f"   Products: {len(products)} - {products}")
            
            return tweet_count > 0
            
        except Exception as e:
            print(f"     Error reading database: {e}")
            return False
    else:
        print(f"  Database not found: {db_path}")
        return False

def check_api_configuration():
    """Check API configuration"""
    print("\n  API Configuration")
    print("=" * 30)
    
    # Check .env file
    if os.path.exists('.env'):
        print("  .env file exists")
    else:
        print("  .env file missing")
    
    # Check bearer token
    bearer_token = os.getenv('BEARER_TOKEN')
    if bearer_token:
        print(f"  Bearer token configured")
        print(f"   Preview: {bearer_token[:10]}...{bearer_token[-4:]}")
        
        # Test API
        try:
            import tweepy
            client = tweepy.Client(bearer_token=bearer_token)
            client.get_me()
            print("  API connection working")
            return True
        except:
            print(" ️ API token configured but not working")
            return False
    else:
        print("  No bearer token found")
        print("   Will use sample data instead")
        return False

def show_next_steps(structure_ok, deps_ok, db_ok, api_ok):
    """Show what user should do next"""
    print("\n  Next Steps")
    print("=" * 30)
    
    if not structure_ok:
        print("1.   Fix project structure")
        print("   Run: python setup.py")
    
    if not deps_ok:
        print("2.   Install dependencies")
        print("   Run: pip install -r requirements.txt")
    
    if not db_ok:
        print("3.   Set up database and collect data")
        print("   Run: python simple_fix.py")
    
    if structure_ok and deps_ok and db_ok:
        print("  Project is ready!")
        print("\n  Available Commands:")
        print("   streamlit run src/app.py        # Launch dashboard")
        print("   python collect_all_data.py      # Get more products")
        print("   python quick_api_check.py       # Check API status")
        
        if not api_ok:
            print("\n  Optional: Enable real Twitter data")
            print("   1. Get token from https://developer.twitter.com/")
            print("   2. Create .env file: echo 'BEARER_TOKEN=your_token' > .env")
            print("   3. Recollect data for real tweets")

def main():
    print("  Product Launch Analyzer - Project Status")
    print("=" * 50)
    
    # Run all checks
    structure_ok = check_project_structure()
    deps_ok = check_dependencies()
    db_ok = check_database_status()
    api_ok = check_api_configuration()
    
    # Show summary
    print("\n  Summary")
    print("=" * 20)
    
    status_items = [
        ("Project Structure", structure_ok),
        ("Dependencies", deps_ok),
        ("Database", db_ok),
        ("API Configuration", api_ok)
    ]
    
    for item, status in status_items:
        icon = " " if status else " "
        print(f"{icon} {item}")
    
    # Show next steps
    show_next_steps(structure_ok, deps_ok, db_ok, api_ok)
    
    # Overall status
    if structure_ok and deps_ok and db_ok:
        print(f"\n  Project Status: READY")
    else:
        print(f"\n ️ Project Status: NEEDS SETUP")

if __name__ == "__main__":
    main()