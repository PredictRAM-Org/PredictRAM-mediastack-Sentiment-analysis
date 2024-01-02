import streamlit as st
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# MediaStack API key
API_KEY = "371a1750c4791037ce0a4d98b7bfd6b9"

# Function to fetch news articles based on the user's stock search
def get_stock_news(stock_symbol):
    base_url = "http://api.mediastack.com/v1/news"
    params = {
        "access_key": API_KEY,
        "keywords": stock_symbol,
        "languages": "en",
        "sort": "published_desc",
    }

    response = requests.get(base_url, params=params)
    return response.json()["data"]

# Function to analyze sentiment using VaderSentiment
def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = analyzer.polarity_scores(text)["compound"]
    return sentiment_score

# Streamlit app
def main():
    st.title("Stock News Sentiment Analysis App")
    
    # User input for stock symbol
    stock_symbol = st.text_input("Enter Stock Symbol:", "AAPL")
    
    if st.button("Get News"):
        # Fetch news articles
        news_data = get_stock_news(stock_symbol)
        
        if not news_data:
            st.warning("No news articles found for the given stock symbol.")
        else:
            # Display news articles and sentiment scores
            st.subheader("Latest News Articles:")
            for news in news_data:
                st.write(f"**Title:** {news['title']}")
                st.write(f"**Source:** {news['source']}")
                st.write(f"**Published:** {news['published_at']}")
                st.write(f"**URL:** {news['url']}")
                
                # Analyze sentiment and display score
                sentiment_score = analyze_sentiment(news['title'])
                st.write(f"**Sentiment Score:** {sentiment_score:.2f}")
                st.write("----")

if __name__ == "__main__":
    main()
