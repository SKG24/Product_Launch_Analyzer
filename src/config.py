import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Application configuration
APP_CONFIG = {
    "name": "Product Launch Analyzer",
    "version": "1.0.0",
    "description": "Social media sentiment analysis for product launches",
    "author": "Your Name"
}

# Database configuration
DATABASE_CONFIG = {
    "db_path": PROJECT_ROOT / "data" / "tweets.db",
    "backup_enabled": True,
    "backup_interval_hours": 24
}

# Twitter API configuration
TWITTER_CONFIG = {
    "bearer_token": os.getenv("BEARER_TOKEN"),
    "rate_limit_delay": 1.0,
    "max_results_per_request": 100,
    "fallback_enabled": True
}

# Sentiment analysis configuration
SENTIMENT_CONFIG = {
    "method": "textblob",  # Options: textblob, vader, ensemble
    "positive_threshold": 0.1,
    "negative_threshold": -0.1,
    "confidence_threshold": 0.5
}

# Data processing configuration
PROCESSING_CONFIG = {
    "batch_size": 100,
    "duplicate_threshold_hours": 24,
    "text_cleaning_enabled": True,
    "min_text_length": 10,
    "max_text_length": 280
}

# Visualization configuration
CHART_CONFIG = {
    "theme": "plotly_white",
    "color_scheme": {
        "positive": "#00CC96",
        "negative": "#EF553B",
        "neutral": "#636EFA"
    },
    "default_height": 400,
    "show_legends": True
}

# Fallback data configuration
FALLBACK_CONFIG = {
    "data_dir": PROJECT_ROOT / "fallback_data",
    "products": [
        "iPhone 15",
        "Galaxy S24", 
        "Pixel 8",
        "OnePlus 12",
        "Nothing Phone"
    ],
    "tweets_per_product": 50,
    "date_range_days": 30
}

# Logging configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "log_file": PROJECT_ROOT / "logs" / "app.log"
}

# Export configuration
EXPORT_CONFIG = {
    "csv_delimiter": ",",
    "date_format": "%Y-%m-%d %H:%M:%S",
    "include_metadata": True
}

def get_database_path():
    """Get the database file path, creating directory if needed"""
    db_path = DATABASE_CONFIG["db_path"]
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return str(db_path)

def get_fallback_data_dir():
    """Get the fallback data directory path"""
    fallback_dir = FALLBACK_CONFIG["data_dir"]
    fallback_dir.mkdir(parents=True, exist_ok=True)
    return fallback_dir

def get_logs_dir():
    """Get the logs directory path, creating if needed"""
    log_file = LOGGING_CONFIG["log_file"]
    log_file.parent.mkdir(parents=True, exist_ok=True)
    return log_file.parent

def validate_config():
    """Validate configuration settings"""
    errors = []
    
    # Check Twitter configuration
    if not TWITTER_CONFIG["bearer_token"] and not TWITTER_CONFIG["fallback_enabled"]:
        errors.append("Twitter bearer token not found and fallback disabled")
    
    # Check required directories
    try:
        get_database_path()
        get_fallback_data_dir()
        get_logs_dir()
    except Exception as e:
        errors.append(f"Directory creation error: {e}")
    
    # Check sentiment configuration
    if SENTIMENT_CONFIG["positive_threshold"] <= SENTIMENT_CONFIG["negative_threshold"]:
        errors.append("Positive threshold must be greater than negative threshold")
    
    return errors

def get_config_summary():
    """Get a summary of current configuration"""
    return {
        "app": APP_CONFIG,
        "database_path": str(DATABASE_CONFIG["db_path"]),
        "twitter_api_enabled": bool(TWITTER_CONFIG["bearer_token"]),
        "fallback_enabled": TWITTER_CONFIG["fallback_enabled"],
        "sentiment_method": SENTIMENT_CONFIG["method"],
        "supported_products": FALLBACK_CONFIG["products"]
    }

# Environment-specific configurations
if os.getenv("ENVIRONMENT") == "development":
    # Development overrides
    LOGGING_CONFIG["level"] = "DEBUG"
    DATABASE_CONFIG["db_path"] = PROJECT_ROOT / "data" / "tweets_dev.db"

elif os.getenv("ENVIRONMENT") == "testing":
    # Testing overrides
    DATABASE_CONFIG["db_path"] = ":memory:"  # In-memory database for tests
    TWITTER_CONFIG["fallback_enabled"] = True
    PROCESSING_CONFIG["batch_size"] = 10

# Validate configuration on import
config_errors = validate_config()
if config_errors:
    import warnings
    for error in config_errors:
        warnings.warn(f"Configuration warning: {error}")