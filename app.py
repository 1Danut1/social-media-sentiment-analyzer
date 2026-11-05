
import streamlit as st
import pandas as pd
import plotly.express as px
from textblob import TextBlob

# Page configuration
st.set_page_config(
    page_title="Social Media Sentiment Analyzer",
    page_icon="📊",
    layout="wide"
)

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("Tweets.csv")

df = load_data()

# Title
st.title("📊 Social Media Sentiment Analyzer")
st.write("Explore customer opinions and sentiment on Twitter.")

st.divider()

# Calculate statistics
total = len(df)
positive = (df["airline_sentiment"] == "positive").sum()
negative = (df["airline_sentiment"] == "negative").sum()
neutral = (df["airline_sentiment"] == "neutral").sum()

# KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Tweets", f"{total:,}")
col2.metric("Positive Tweets", f"{positive:,}")
col3.metric("Negative Tweets", f"{negative:,}")
col4.metric("Neutral Tweets", f"{neutral:,}")

st.divider()

# Sentiment distribution
st.subheader("Overall Sentiment Distribution")

sentiment_counts = df["airline_sentiment"].value_counts()

colors = {
    "positive": "#2ECC71",
    "negative": "#E74C3C",
    "neutral": "#F1C40F"
}

fig = px.pie(
    names=sentiment_counts.index,
    values=sentiment_counts.values,
    color=sentiment_counts.index,
    color_discrete_map=colors,
    hole=0.4
)

st.plotly_chart(fig, use_container_width=True)

# Airline comparison
st.subheader("Sentiment Analysis by Airline")

airline_data = pd.crosstab(
    df["airline"],
    df["airline_sentiment"]
)

fig2 = px.bar(
    airline_data,
    barmode="group",
    color_discrete_map=colors,
    labels={
        "value": "Number of Tweets",
        "airline": "Airline"
    }
)

st.plotly_chart(fig2, use_container_width=True)

# Custom sentiment analysis
st.divider()
st.subheader("Try Your Own Comment")

comment = st.text_area(
    "Enter a comment in English:",
    placeholder="Write your comment here..."
)

if st.button("Analyze Sentiment"):
    if comment.strip():

        polarity = TextBlob(comment).sentiment.polarity

        if polarity > 0.1:
            result = "Positive 😊"
            st.success(f"Predicted sentiment: {result}")

        elif polarity < -0.1:
            result = "Negative 😞"
            st.error(f"Predicted sentiment: {result}")

        else:
            result = "Neutral 😐"
            st.info(f"Predicted sentiment: {result}")

        st.write(f"Polarity score: {polarity:.2f}")

    else:
        st.warning("Please enter a comment first.")