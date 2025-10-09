import streamlit as st
import sys
import os
from textblob import TextBlob

# Add backend folder to sys.path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from fetch_news import fetch_live_news, store_articles

st.set_page_config(page_title="NewsPulse Dashboard", page_icon="📰", layout="wide")

# Custom dark theme + styling
st.markdown("""
<style>
    .main {background-color: #1e1e23; color: #f3f3ef;}
    .stTextInput>div>div>input {
        background-color: #23243a !important;
        color: white !important;
        border-radius: 7px;
        padding: 8px;
    }
    .stButton>button {
        background-color: #6366f1 !important;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.4rem 1rem;
        font-size: 16px;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #4f46e5 !important;
    }
    hr {
        border-color: #44475a;
        margin: 2rem 0;
    }
    .news-card {
        background-color: #27293d;
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 1rem;
    }
    .news-title {
        font-weight: 700;
        font-size: 18px;
        margin-bottom: 6px;
    }
    .news-source, .news-date {
        font-size: 12px;
        color: #aaaaff;
    }
    .news-desc {
        font-size: 14px;
        margin-top: 8px;
        color: #ddd;
    }
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("# 📰 NewsPulse Dashboard")
    st.write("Search live news by topic and store preprocessed news automatically.")

    topic = st.text_input("🔎 Enter topic", placeholder="e.g. climate, finance, crime")

    # Auto spell correction
    corrected_topic = topic
    if topic.strip():
        corrected = str(TextBlob(topic).correct())
        if corrected.lower() != topic.lower():
            st.info(f"Did you mean: {corrected}? Searching for corrected topic.")
            corrected_topic = corrected

    num_articles = st.slider("Number of articles", 5, 50, 10)

    if st.button("Fetch News"):
        if not corrected_topic.strip():
            st.warning("Please enter a valid topic to search.")
        else:
            articles = fetch_live_news(corrected_topic, num_articles)
            if not articles:
                st.info("No results for this topic.")
            else:
                st.markdown("---")
                for idx, article in enumerate(articles, 1):
                    with st.container():
                        st.markdown('<div class="news-card">', unsafe_allow_html=True)
                        st.markdown(f'<div class="news-title">{idx}. {article.get("title", "")}</div>', unsafe_allow_html=True)
                        if article.get("urlToImage"):
                            st.image(article["urlToImage"], use_container_width=True, caption=article.get("source", {}).get("name", ""))
                        st.markdown(f'<div class="news-source">Source: {article.get("source", {}).get("name", "Unknown")}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="news-date">Published: {article.get("publishedAt", "")}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="news-desc">{article.get("description", "")}</div>', unsafe_allow_html=True)
                        if article.get("url"):
                            st.markdown(f'[Read more]({article.get("url")})')
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.markdown("")
                store_articles(articles)
                st.success(f"Stored {len(articles)} articles successfully.")

st.markdown("""
<hr>
<center style="color:#6366F1; font-size: 15px;">Powered by NewsAPI | Built with Streamlit</center>
""", unsafe_allow_html=True)
