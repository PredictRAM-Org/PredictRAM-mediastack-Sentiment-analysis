import streamlit as st
import requests
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# MediaStack API key
API_KEY = "371a1750c4791037ce0a4d98b7bfd6b9"

# Function to fetch business and finance news for sentiment analysis
def get_business_finance_news(stock_symbol):
    base_url = "http://api.mediastack.com/v1/news"
    params = {
        "access_key": API_KEY,
        "keywords": stock_symbol,
        "categories": "business",
        "countries": "in",
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

    # User input for multiple stock symbols
    stock_symbols = st.text_input("Enter Stock Symbols (comma-separated):", "AAPL,GOOGL,MSFT").split(',')

    if st.button("Get News"):
        # Display table header
        st.subheader("Stock News Sentiment Analysis")

        # Create a dataframe to store stock and sentiment data
        stock_sentiments = {"Stock Symbol": [], "Sentiment Score": []}

        # Fetch news and analyze sentiment for each stock
        for stock_symbol in stock_symbols:
            news_data = get_business_finance_news(stock_symbol)

            if not news_data:
                st.warning(f"No news articles found for {stock_symbol}.")
            else:
                # Analyze sentiment for each article and calculate average score
                sentiment_scores = [analyze_sentiment(news['title']) for news in news_data]
                average_sentiment = sum(sentiment_scores) / len(sentiment_scores)

                # Display stock symbol, average sentiment, and individual news articles
                st.subheader(f"{stock_symbol} - Average Sentiment Score: {average_sentiment:.2f}")

                for i, news in enumerate(news_data):
                    st.write(f"**Title:** {news['title']}")
                    st.write(f"**Source:** {news['source']}")
                    st.write(f"**Published:** {news['published_at']}")
                    st.write(f"**URL:** {news['url']}")
                    st.write(f"**Sentiment Score:** {sentiment_scores[i]:.2f}")
                    st.write("----")

                # Append data to the dataframe
                stock_sentiments["Stock Symbol"].append(stock_symbol)
                stock_sentiments["Sentiment Score"].append(average_sentiment)

        # Display table with stock sentiment data
        sentiment_df = pd.DataFrame(stock_sentiments)
        st.table(sentiment_df)

if __name__ == "__main__":
    main()
