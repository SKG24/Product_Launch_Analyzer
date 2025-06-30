import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Import our modules
from database import get_all_tweets
from charts import create_sentiment_chart, create_volume_chart, create_pie_chart
from utils import filter_tweets_by_date, calculate_metrics

# Page setup
st.set_page_config(page_title="Product Launch Analyzer", layout="wide")
st.title("  Product Launch Sentiment Analysis")

# Load data
@st.cache_data
def load_data():
    tweets = get_all_tweets()
    if tweets:
        df = pd.DataFrame(tweets)
        return df
    return pd.DataFrame()

# Main app
def main():
    df = load_data()
    
    if df.empty:
        st.warning("No data found. Please run the pipeline first.")
        st.info("Run: `python scripts/run_pipeline.py`")
        return
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Product selection
    products = df['product'].unique()
    selected_product = st.sidebar.selectbox("Select Product", products)
    
    # Date range
    min_date = df['created_at'].min()
    max_date = df['created_at'].max()
    
    date_range = st.sidebar.date_input(
        "Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    # Filter data
    filtered_df = df[df['product'] == selected_product]
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filter_tweets_by_date(filtered_df, start_date, end_date)
    
    # Show metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Tweets", len(filtered_df))
    
    with col2:
        avg_sentiment = filtered_df['sentiment'].mean()
        st.metric("Avg Sentiment", f"{avg_sentiment:.3f}")
    
    with col3:
        positive_tweets = len(filtered_df[filtered_df['sentiment'] > 0.1])
        positive_pct = (positive_tweets / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0
        st.metric("Positive %", f"{positive_pct:.1f}%")
    
    with col4:
        avg_likes = filtered_df['likes'].mean()
        st.metric("Avg Likes", f"{avg_likes:.1f}")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        sentiment_fig = create_sentiment_chart(filtered_df)
        if sentiment_fig:
            st.plotly_chart(sentiment_fig, use_container_width=True)
    
    with col2:
        pie_fig = create_pie_chart(filtered_df)
        if pie_fig:
            st.plotly_chart(pie_fig, use_container_width=True)
    
    # Volume chart
    volume_fig = create_volume_chart(filtered_df)
    if volume_fig:
        st.plotly_chart(volume_fig, use_container_width=True)
    
    # Sample tweets
    st.subheader("Recent Tweets")
    sample_tweets = filtered_df.head(5)[['created_at', 'text', 'sentiment', 'likes']]
    st.dataframe(sample_tweets)

if __name__ == "__main__":
    main()