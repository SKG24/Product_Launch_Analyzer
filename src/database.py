import sqlite3
import pandas as pd
from datetime import datetime
import os

# Find project root directory consistently
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)  # Go up one level from src/
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

# Create data directory if it doesn't exist
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

DATABASE_PATH = os.path.join(DATA_DIR, "tweets.db")

def create_connection():
    """Create database connection"""
    return sqlite3.connect(DATABASE_PATH)

def create_table():
    """Create tweets table if it doesn't exist"""
    conn = create_connection()
    cursor = conn.cursor()
    
    # Check if table exists and get its schema
    cursor.execute("PRAGMA table_info(tweets)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'user_id' not in columns and columns:
        # Table exists but missing user_id column - add it
        print("Adding missing user_id column to existing table...")
        cursor.execute("ALTER TABLE tweets ADD COLUMN user_id TEXT DEFAULT 'unknown'")
    elif not columns:
        # Table doesn't exist - create it
        print("Creating new tweets table...")
        cursor.execute('''
            CREATE TABLE tweets (
                id TEXT PRIMARY KEY,
                created_at TEXT,
                text TEXT,
                user_id TEXT DEFAULT 'unknown',
                likes INTEGER DEFAULT 0,
                retweets INTEGER DEFAULT 0,
                sentiment REAL,
                product TEXT
            )
        ''')
    else:
        print("Table already exists with correct schema")
    
    conn.commit()
    conn.close()

def insert_tweets(tweets):
    """Insert tweets into database"""
    conn = create_connection()
    cursor = conn.cursor()
    
    for tweet in tweets:
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO tweets 
                (id, created_at, text, user_id, likes, retweets, sentiment, product)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                tweet.get('id'),
                tweet.get('created_at'),
                tweet.get('text'),
                tweet.get('user_id', 'unknown'),
                tweet.get('likes', 0),
                tweet.get('retweets', 0),
                tweet.get('sentiment', 0),
                tweet.get('product')
            ))
        except Exception as e:
            print(f"Error inserting tweet: {e}")
    
    conn.commit()
    conn.close()
    print(f"Inserted {len(tweets)} tweets")

def get_all_tweets():
    """Get all tweets from database"""
    try:
        conn = create_connection()
        
        query = """
            SELECT id, created_at, text, user_id, likes, retweets, sentiment, product
            FROM tweets 
            ORDER BY created_at DESC
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        # Convert to list of dictionaries
        return df.to_dict('records')
    
    except Exception as e:
        print(f"Error getting tweets: {e}")
        return []

def get_tweets_by_product(product):
    """Get tweets for specific product"""
    try:
        conn = create_connection()
        
        query = """
            SELECT * FROM tweets 
            WHERE product = ?
            ORDER BY created_at DESC
        """
        
        df = pd.read_sql_query(query, conn, params=[product])
        conn.close()
        
        return df.to_dict('records')
    
    except Exception as e:
        print(f"Error getting tweets for {product}: {e}")
        return []

def count_tweets():
    """Count total tweets in database"""
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM tweets")
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
    
    except Exception as e:
        print(f"Error counting tweets: {e}")
        return 0

def get_products():
    """Get list of all products"""
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT DISTINCT product FROM tweets WHERE product IS NOT NULL")
        products = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return products
    
    except Exception as e:
        print(f"Error getting products: {e}")
        return []

# Initialize database when module is imported
if __name__ == "__main__":
    create_table()
    print("Database initialized")