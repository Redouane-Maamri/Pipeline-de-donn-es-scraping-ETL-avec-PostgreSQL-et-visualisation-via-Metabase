import pandas as pd
import psycopg2

def load_to_db():
    conn = psycopg2.connect(
        host="localhost",
        database="news_db",
        user="postgres",
        password=""  # put your password if needed
    )

    cursor = conn.cursor()

    # ----------------------
    # LOAD ARTICLES (SILVER)
    # ----------------------
    df = pd.read_csv("data/silver/articles_cleaned.csv")

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO articles (title, content, source, word_count)
            VALUES (%s, %s, %s, %s)
        """, (row["title"], row["content"], row["source"], row["word_count"]))

    print("Articles loaded ✅")

    # ----------------------
    # LOAD KEYWORDS (GOLD)
    # ----------------------
    keywords_df = pd.read_csv("data/gold/top_keywords.csv")

    # Optional: clean old data (VERY IMPORTANT)
    cursor.execute("DELETE FROM keywords")

    for _, row in keywords_df.iterrows():
        cursor.execute("""
            INSERT INTO keywords (word, count)
            VALUES (%s, %s)
        """, (row["word"], row["count"]))

    print("Keywords loaded ✅")

    # ----------------------
    # FINAL COMMIT
    # ----------------------
    conn.commit()
    conn.close()

    print("Data loaded to PostgreSQL 🚀")