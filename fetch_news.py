#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from dotenv import load_dotenv
import requests
import mysql.connector
from datetime import datetime

load_dotenv()

def connect_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB")
    )

def convert_publishedAt(publishedAt_str):
    try:
        dt = datetime.strptime(publishedAt_str, "%Y-%m-%dT%H:%M:%SZ")
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return None

def insert_news(article):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(1) FROM news WHERE url = %s", (article.get("url"),))
    exists = cursor.fetchone()[0]

    if exists:
        # Skip duplicates
        cursor.close()
        conn.close()
        return

    published = convert_publishedAt(article.get("publishedAt"))
    cursor.execute(
        "INSERT INTO news (title, source, publishedAt, url, description, imageurl) VALUES (%s, %s, %s, %s, %s, %s)",
        (
            article.get("title"),
            article.get("source", {}).get("name"),
            published,
            article.get("url"),
            article.get("description"),
            article.get("urlToImage"),
        )
    )
    conn.commit()
    cursor.close()
    conn.close()

def fetch_and_store_for_topic(topic):
    NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
    url = f"https://newsapi.org/v2/everything?q={topic}&pageSize=10&apiKey={NEWSAPI_KEY}"
    response = requests.get(url)
    data = response.json()
    articles = data.get("articles", [])
    print(f"Fetched {len(articles)} articles for topic '{topic}'. Inserting up to 20...")
    for article in articles[:20]:
        if article.get("title"):
            insert_news(article)
    print("Insertion complete.")

if __name__ == "__main__":
    admin_choice = input("Admin: Do you want to fetch news for a topic? (y/n): ").strip().lower()
    if admin_choice == 'y':
        topic = input("Enter a topic to fetch news for: ")
        fetch_and_store_for_topic(topic)
    else:
        print("Skipping news fetch for this run.")


# In[ ]:




