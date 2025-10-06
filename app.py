#!/usr/bin/env python
# coding: utf-8

# In[4]:


import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def connect_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB")
    )

def get_trending_topics(limit=10):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT source
        FROM news
        WHERE source IS NOT NULL
        ORDER BY source
        LIMIT %s
    """, (limit,))
    topics = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return topics

def getnewsbytopic(topic, limit=20):
    conn = connect_db()
    query = """
        SELECT title, source, publishedAt, url, description, imageurl
        FROM news
        WHERE title LIKE %s OR description LIKE %s
        ORDER BY publishedAt DESC
        LIMIT %s
    """
    pattern = f"%{topic}%"
    df = pd.read_sql_query(query, conn, params=(pattern, pattern, limit))
    conn.close()
    return df

def get_total_articles_for_topic(topic):
    conn = connect_db()
    cursor = conn.cursor()
    query = """
        SELECT COUNT(*)
        FROM news
        WHERE title LIKE %s OR description LIKE %s
    """
    pattern = f"%{topic}%"
    cursor.execute(query, (pattern, pattern))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count

def format_datetime(dt):
    try:
        dt = pd.to_datetime(dt)
        return dt.strftime("%B %d, %Y %H:%M")
    except:
        return ""

def main():
    st.set_page_config(page_title="NewsPulse Dashboard", page_icon="📰", layout="wide")
    st.markdown("""
    <style>
    .main-header {
        font-size: 36px;
        font-weight: bold;
        color: #ff6f61;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 18px;
        color: #cccccc;
        margin-top: 0px;
        margin-bottom: 20px;
    }
    .info-box {
        background: linear-gradient(90deg,#0f4d8d, #037ffc 80%);
        color: white;
        padding: 10px;
        border-radius: 8px;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .article-container {
        background-color: #222;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 25px;
        color: #ddd;
    }
    .article-title {
        color: #ff6f61;
        font-size: 22px;
        font-weight: 700;
    }
    .article-meta {
        font-style: italic;
        font-size: 15px;
        color: #aaa;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown('<div class="main-header">📰 NewsPulse Dashboard</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Fetch and explore the latest news based on your topics.</div>', unsafe_allow_html=True)
        st.markdown('<div class="info-box">This dashboard only reads from the database. Enjoy exploring trending topics!</div>', unsafe_allow_html=True)

        # Use a Streamlit form for search bar with search button
        with st.form("search_form"):
            user_topic = st.text_input("Enter a topic/keyword to search news:", key="topic_input")
            search_submit = st.form_submit_button("Search")

        sources = get_trending_topics()
        selected_source = None

        if not user_topic and sources:
            st.markdown("### 📌 Trending News Sources")
            selected_source = st.selectbox(
                "Or select a trending source to explore:",
                sources if sources else ["No sources found"], key="source_select"
            )

        max_articles = st.slider("Select number of articles to display", min_value=1, max_value=20, value=5, step=1)
        topic_for_search = user_topic if user_topic else selected_source

        # Only show articles after clicking search OR selecting a source (when no text input)
        if (search_submit and topic_for_search) or (not user_topic and selected_source):
            total_articles = get_total_articles_for_topic(topic_for_search)
            if max_articles > total_articles:
                st.info(f"Only {total_articles} articles available for topic '{topic_for_search}'. Showing all available.")
                max_articles = total_articles

            st.markdown(f"### 🔎 News Articles for: **{topic_for_search}**")
            news_df = getnewsbytopic(topic_for_search, max_articles)
            if news_df.empty:
                st.warning("No articles found related to this topic. Try another topic or keyword.")
            else:
                for _, row in news_df.iterrows():
                    st.markdown('<div class="article-container">', unsafe_allow_html=True)
                    if row["imageurl"]:
                        st.image(row["imageurl"], use_container_width=True)  # Full-width image
                    st.markdown(f'<div class="article-title"><a href="{row["url"]}" target="_blank" style="color:#ff6f61;text-decoration:none;">{row["title"]}</a></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="article-meta">📍 {row["source"]} | ⏰ {format_datetime(row["publishedAt"])}</div>', unsafe_allow_html=True)
                    if row["description"]:
                        st.write(row["description"])
                    st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("***")

if __name__ == "__main__":
    main()


# In[ ]:




