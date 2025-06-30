import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

def create_sentiment_chart(df):
    """Create sentiment over time line chart"""
    try:
        if df.empty:
            return None
        
        # Convert created_at to datetime
        df['date'] = pd.to_datetime(df['created_at']).dt.date
        
        # Group by date and calculate average sentiment
        daily_sentiment = df.groupby('date')['sentiment'].mean().reset_index()
        
        # Create line chart
        fig = px.line(
            daily_sentiment,
            x='date',
            y='sentiment',
            title='Sentiment Over Time',
            labels={'sentiment': 'Average Sentiment', 'date': 'Date'}
        )
        
        # Add horizontal line at y=0 (neutral)
        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        
        return fig
    
    except Exception as e:
        print(f"Error creating sentiment chart: {e}")
        return None

def create_volume_chart(df):
    """Create tweet volume bar chart"""
    try:
        if df.empty:
            return None
        
        # Convert created_at to datetime
        df['date'] = pd.to_datetime(df['created_at']).dt.date
        
        # Count tweets per day
        daily_volume = df.groupby('date').size().reset_index(name='count')
        
        # Create bar chart
        fig = px.bar(
            daily_volume,
            x='date',
            y='count',
            title='Tweet Volume Over Time',
            labels={'count': 'Number of Tweets', 'date': 'Date'}
        )
        
        return fig
    
    except Exception as e:
        print(f"Error creating volume chart: {e}")
        return None

def create_pie_chart(df):
    """Create sentiment distribution pie chart"""
    try:
        if df.empty:
            return None
        
        # Categorize sentiments
        def categorize_sentiment(score):
            if score > 0.1:
                return 'Positive'
            elif score < -0.1:
                return 'Negative'
            else:
                return 'Neutral'
        
        df['sentiment_category'] = df['sentiment'].apply(categorize_sentiment)
        
        # Count each category
        sentiment_counts = df['sentiment_category'].value_counts()
        
        # Create pie chart
        fig = px.pie(
            values=sentiment_counts.values,
            names=sentiment_counts.index,
            title='Sentiment Distribution',
            color_discrete_map={
                'Positive': '#00CC96',
                'Negative': '#EF553B',
                'Neutral': '#636EFA'
            }
        )
        
        return fig
    
    except Exception as e:
        print(f"Error creating pie chart: {e}")
        return None

def create_engagement_chart(df):
    """Create engagement vs sentiment scatter plot"""
    try:
        if df.empty:
            return None
        
        # Calculate total engagement
        df['total_engagement'] = df['likes'] + df['retweets']
        
        # Create scatter plot
        fig = px.scatter(
            df,
            x='sentiment',
            y='total_engagement',
            title='Engagement vs Sentiment',
            labels={
                'sentiment': 'Sentiment Score',
                'total_engagement': 'Total Engagement (Likes + Retweets)'
            },
            hover_data=['text']
        )
        
        # Add vertical line at sentiment=0
        fig.add_vline(x=0, line_dash="dash", line_color="gray")
        
        return fig
    
    except Exception as e:
        print(f"Error creating engagement chart: {e}")
        return None

def create_product_comparison_chart(df):
    """Create product comparison bar chart"""
    try:
        if df.empty:
            return None
        
        # Calculate average sentiment by product
        product_sentiment = df.groupby('product')['sentiment'].mean().reset_index()
        
        # Create bar chart
        fig = px.bar(
            product_sentiment,
            x='product',
            y='sentiment',
            title='Average Sentiment by Product',
            labels={'sentiment': 'Average Sentiment', 'product': 'Product'}
        )
        
        # Add horizontal line at y=0
        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        
        return fig
    
    except Exception as e:
        print(f"Error creating comparison chart: {e}")
        return None

# Test the chart functions
if __name__ == "__main__":
    # Create sample data for testing
    sample_data = {
        'created_at': ['2024-01-01', '2024-01-02', '2024-01-03'] * 3,
        'sentiment': [0.5, -0.3, 0.1, 0.8, -0.6, 0.2, 0.3, -0.2, 0.0],
        'likes': [10, 5, 8, 15, 3, 12, 9, 6, 7],
        'retweets': [2, 1, 3, 5, 0, 4, 2, 1, 2],
        'product': ['iPhone 15'] * 3 + ['Galaxy S24'] * 3 + ['Pixel 8'] * 3,
        'text': ['Great phone!', 'Not good', 'Okay product'] * 3
    }
    
    df = pd.DataFrame(sample_data)
    
    print("Testing chart creation...")
    
    # Test each chart function
    charts = [
        ('Sentiment Chart', create_sentiment_chart),
        ('Volume Chart', create_volume_chart),
        ('Pie Chart', create_pie_chart),
        ('Engagement Chart', create_engagement_chart),
        ('Comparison Chart', create_product_comparison_chart)
    ]
    
    for name, func in charts:
        try:
            fig = func(df)
            if fig:
                print(f"✓ {name} created successfully")
            else:
                print(f"✗ {name} failed")
        except Exception as e:
            print(f"✗ {name} error: {e}")