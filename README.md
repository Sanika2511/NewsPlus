# 📰 NewsPulse

A full-stack project to fetch, store, and display the latest news by topic using **NewsAPI**, **Python**, **MySQL**, and **Streamlit**, with secure credential management using **.env files**.

---

## 📋 Project Overview

**NewsPulse** enables users to:

* Fetch the latest news for any topic using **NewsAPI**.
* Store fetched data securely in a **MySQL database**.
* Explore and visualize the news interactively using a **Streamlit dashboard**.

All API keys and database credentials are stored securely in a .env file to prevent exposure in the codebase.

---

## 🧩 Architecture

```
fetch_news.py → Fetches news via NewsAPI → Stores in MySQL
app.py        → Fetches from MySQL → Displays in Streamlit dashboard
```

* **Backend (`fetch_news.py`):**

  * Calls NewsAPI using the API key from `.env`.
  * Inserts fetched news into MySQL, skipping duplicates.
* **Frontend (`app.py`):**

  * Connects to the same database.
  * Displays an interactive dashboard with search and trending topics.

---

## ⚙️ Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Sanika2511/NewsPulse.git
cd NewsPulse
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate   # macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` File

In the root directory, create a `.env` file to securely store your credentials:

```
NEWSAPI_KEY=your_newsapi_key_here
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=your_mysql_username
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=newsdb
```

## 🗃️ Database Setup

Run the following in your MySQL shell:

```sql
CREATE DATABASE newsdb;
USE newsdb;

CREATE TABLE news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title TEXT,
    source VARCHAR(255),
    publishedAt DATETIME,
    url TEXT UNIQUE,
    description TEXT,
    imageurl TEXT
);
```

---

## 🚀 How to Run

### Backend — Fetch News

```bash
python fetch_news.py
```

* Prompts admin to enter a topic.
* Fetches news using NewsAPI.
* Stores new articles in MySQL.

### Frontend — Launch Dashboard

```bash
streamlit run app.py
```

Then open the app in your browser:
👉 **[http://localhost:8501](http://localhost:8501)**

---

## 🧠 Tech Stack

| Component | Technology                      |
| --------- | ------------------------------- |
| Language  | Python                          |
| Frontend  | Streamlit                       |
| Backend   | Python (Requests, dotenv)       |
| Database  | MySQL                           |
| API       | NewsAPI                         |
| Libraries | Pandas, MySQL Connector, dotenv |

---

## ✨ Features

✅ Fetch and store news by topic/keyword
✅ Skip duplicate articles during insertion
✅ Securely manage API keys and DB credentials using `.env`
✅ Explore trending sources from stored articles
✅ Interactive Streamlit dashboard with search and filters
✅ Dark-themed responsive UI

---

## 📊 Dashboard Preview

* Enter a keyword or choose a trending source
* View articles with title, date, image, description, and direct link
* Adjust number of articles displayed using a slider

---

## 🧾 License

This project is licensed under the **MIT License**.

---

## 👩‍💻 Author

**Sanika Sharma**
MSc Statistics | Data Analyst | Python Developer
