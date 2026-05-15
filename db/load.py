import pandas as pd
import psycopg2


def load_to_db():

    conn = psycopg2.connect(
        host="postgres",
        database="news_db",
        user="postgres",
        password="postgres"
    )

    cursor = conn.cursor()

    # ----------------------
    # CREATE TABLES IF NOT EXISTS
    # ----------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        id SERIAL PRIMARY KEY,
        title TEXT,
        content TEXT,
        source VARCHAR(50),
        word_count INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS keywords (
        id SERIAL PRIMARY KEY,
        word TEXT,
        count INTEGER,
        source VARCHAR(50)
    )
    """)

    # ----------------------
    # LOAD ARTICLES (SILVER)
    # ----------------------

    df = pd.read_csv(
        "data/silver/articles_cleaned.csv"
    )

    # Clean old articles
    cursor.execute("DELETE FROM articles")

    for _, row in df.iterrows():

        cursor.execute("""
            INSERT INTO articles (
                title,
                content,
                source,
                word_count
            )
            VALUES (%s, %s, %s, %s)
        """, (
            row["title"],
            row["content"],
            row["source"],
            row["word_count"]
        ))

    print("Articles loaded ✅")

    # ----------------------
    # LOAD KEYWORDS (GOLD)
    # ----------------------

    keywords_df = pd.read_csv(
        "data/gold/top_keywords.csv"
    )

    # Clean old keywords
    cursor.execute("DELETE FROM keywords")

    for _, row in keywords_df.iterrows():

        cursor.execute("""
            INSERT INTO keywords (
                word,
                count,
                source
            )
            VALUES (%s, %s, %s)
        """, (
            row["word"],
            row["count"],
            row["source"]
        ))

    print("Keywords loaded ✅")

    # ----------------------
    # FINAL COMMIT
    # ----------------------

    conn.commit()
    conn.close()

    print("Data loaded to PostgreSQL 🚀")