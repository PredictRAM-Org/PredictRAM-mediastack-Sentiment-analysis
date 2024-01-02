import streamlit as st
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# MediaStack API key
API_KEY = "371a1750c4791037ce0a4d98b7bfd6b9"

# Function to fetch business and finance news for sentiment analysis
def get_business_finance_news():
    base_url = "http://api.mediastack.com/v1/news"
    params = {
        "access_key": API_KEY,
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
    st.title("Indian Business and Finance News Sentiment Analysis App")

    if st.button("Get News"):
        # Fetch business and finance news
        news_data = get_business_finance_news()

        if not news_data:
            st.warning("No business and finance news articles found.")
        else:
            # Display news articles and sentiment scores
            st.subheader("Latest Business and Finance News Articles:")
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
