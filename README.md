# Product Launch Analyzer 📱

A comprehensive sentiment analysis platform for monitoring social media reactions to product launches. This project demonstrates end-to-end data engineering, natural language processing, and business intelligence capabilities through an interactive web dashboard.

## 🎯 Project Overview

Product Launch Analyzer helps companies understand customer sentiment around new product releases by:
- **Collecting** social media data from Twitter API with intelligent fallback
- **Processing** text data using advanced NLP techniques  
- **Analyzing** sentiment patterns and trends over time
- **Visualizing** insights through interactive charts and dashboards
- **Storing** processed data for historical analysis

### Business Value
- **Real-time Monitoring**: Track customer reactions as they happen
- **Competitive Analysis**: Compare sentiment across different products
- **Strategic Insights**: Data-driven decisions for marketing and product teams
- **Trend Identification**: Spot emerging issues or positive momentum early

## 🏗️ Technical Architecture

```
Data Collection → Processing → Analysis → Visualization → Storage
     ↓              ↓          ↓           ↓            ↓
  Twitter API   Text Cleaning  Sentiment  Interactive   SQLite
  + Fallback    + Validation   Analysis   Dashboard    Database
```

### Core Components

1. **Data Ingestion Layer** (`tweet_collector.py`)
2. **Processing Engine** (`data_processor.py`, `sentiment_analyzer.py`)
3. **Storage Layer** (`database.py`)
4. **Visualization Layer** (`charts.py`, `app.py`)
5. **Orchestration Layer** (`pipeline.py`)

## 📊 Usage Examples

### Basic Pipeline Execution
```python
# Collect and analyze data for a single product
from src.pipeline import run_pipeline_for_product

result = run_pipeline_for_product("iPhone 15", tweet_count=50)
print(f"Processed {result['tweets_stored']} tweets")
```

### Custom Sentiment Analysis
```python
from src.sentiment_analyzer import analyze_sentiment

# Analyze custom text
text = "The new iPhone camera is absolutely incredible!"
score = analyze_sentiment(text)
print(f"Sentiment score: {score:.3f}")  # Output: 0.625 (positive)
```

### Data Filtering and Analysis
```python
from src.utils import filter_tweets_by_date, calculate_metrics
from datetime import date, timedelta

# Filter tweets by date range
start_date = date.today() - timedelta(days=7)
end_date = date.today()
recent_tweets = filter_tweets_by_date(tweets, "iPhone 15", [start_date, end_date])

# Calculate metrics
metrics = calculate_metrics(recent_tweets)
print(f"Average sentiment: {metrics['avg_sentiment']:.3f}")
print(f"Positive tweets: {metrics['positive_tweets']}")
```


## 🔧 Key Features

### 1. **Intelligent Data Collection**
- Primary: Twitter API integration with authentication
- Fallback: Realistic sample data generation
- Rate limiting and error handling
- Automatic retry mechanisms

### 2. **Text Processing**
```python
def clean_text(text):
    # Remove URLs, mentions, hashtags
    text = re.sub(r'http\S+|@\w+|#\w+', '', text)
    # Normalize whitespace
    text = ' '.join(text.split())
    return text.strip()
```

### 3. **Sentiment Analysis Pipeline**
- Text preprocessing and cleaning
- Polarity scoring (-1 to +1 scale)
- Confidence measurement
- Batch processing capabilities

### 4. **Interactive Dashboard**
- Real-time filtering by product and date
- Multiple visualization types
- Export functionality (CSV download)
- Responsive design for different screen sizes

### 5. **Data Persistence**
- SQLite database for local storage
- Automatic schema management
- Data validation and integrity checks
- Backup and recovery utilities

## 📈 Sample Outputs

### Dashboard Metrics
```
📊 iPhone 15 Analysis (Last 7 Days)
├── Total Tweets: 1,247
├── Average Sentiment: 0.342 (Positive)
├── Positive %: 65.2%
└── Peak Day: 2024-01-15 (89 tweets)
```

### Sentiment Analysis Results
```python
{
    "product": "iPhone 15",
    "total_tweets": 1247,
    "sentiment_distribution": {
        "positive": 813,    # 65.2%
        "neutral": 298,     # 23.9%
        "negative": 136     # 10.9%
    },
    "average_sentiment": 0.342,
    "peak_engagement_day": "2024-01-15"
}
```

## 🧪 Testing

### Run Unit Tests
```bash
# Run all tests
python tests/test_basic.py


### Test Coverage
- Sentiment analysis accuracy
- Database operations
- Data processing functions
- Utility function validation
- Error handling scenarios

## 🚀 Deployment Options

### Local Development
```bash
streamlit run src/app.py --server.port 8501
```

### Production Deployment
```bash
# Using Streamlit Cloud
# 1. Push to GitHub
# 2. Connect to Streamlit Cloud
# 3. Deploy automatically

## 🔍 Monitoring & Debugging

### API Status Check
```bash
python utility_scripts/quick_api_check.py
```

### Database Diagnostics
```bash
python utility_scripts/debug.py
```

---
