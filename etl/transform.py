import pandas as pd
import json
from collections import Counter

def transform():
    # ----------------------
    # LOAD BRONZE DATA
    # ----------------------
    with open("data/bronze/articles.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    # ----------------------
    # CLEANING (SILVER)
    # ----------------------

    # Remove empty content
    df = df[df["content"].notnull()]
    df = df[df["content"] != ""]

    # Remove extra spaces
    df["content"] = df["content"].str.replace("\n", " ")
    df["content"] = df["content"].str.strip()

    # Remove noise (newsletter, comments, etc.)
    noise_words = ["اشترك الآن", "البريد الإلكتروني", "التعليق", "النشرة البريدية"]

    for word in noise_words:
        df["content"] = df["content"].str.replace(word, "")

    # Add feature: word count
    df["word_count"] = df["content"].apply(lambda x: len(x.split()))

    # Keep only real articles
    df = df[df["word_count"] > 150]

    # Remove duplicates
    df = df.drop_duplicates(subset=["title"])

    # Remove weak titles
    df = df[df["title"].str.len() > 10]

    # Save Silver
    df.to_csv("data/silver/articles_cleaned.csv", index=False)
    print("Silver layer created ✅")

    # ----------------------
    # GOLD LAYER (ANALYTICS)
    # ----------------------

    # 1. Metrics (articles per source)
    metrics = df.groupby("source").size().reset_index(name="article_count")
    metrics.to_csv("data/gold/metrics.csv", index=False)
    print("Gold metrics created ✅")

    # 2. Top Keywords
    all_text = " ".join(df["content"])
    words = all_text.split()

    # Remove useless words
    stop_words = ["في", "من", "على", "و", "الى", "إلى", "عن", "أن", "هذا", "الذي", "التي", "كان"]

    words = [w for w in words if w not in stop_words and len(w) > 2]

    # Count frequency
    word_counts = Counter(words)
    top_words = word_counts.most_common(10)

    keywords_df = pd.DataFrame(top_words, columns=["word", "count"])
    keywords_df.to_csv("data/gold/top_keywords.csv", index=False)

    print("Top keywords created ✅")