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

    # Remove noise
    noise_words = [
        "اشترك الآن",
        "البريد الإلكتروني",
        "التعليق",
        "النشرة البريدية"
    ]

    for word in noise_words:
        df["content"] = df["content"].str.replace(word, "")

    # Add feature: word count
    df["word_count"] = df["content"].apply(
        lambda x: len(x.split())
    )

    # Keep only real articles
    df = df[df["word_count"] > 150]

    # Remove duplicates
    df = df.drop_duplicates(subset=["title"])

    # Remove weak titles
    df = df[df["title"].str.len() > 10]

    
    df.to_csv(
        "data/silver/articles_cleaned.csv",
        index=False
    )

    print("Silver layer created ✅")


    
    metrics = df.groupby("source").size().reset_index(
        name="article_count"
    )

    metrics.to_csv(
        "data/gold/metrics.csv",
        index=False
    )

    print("Gold metrics created ✅")

    # ----------------------
    # 2️⃣ TOP KEYWORDS PER SOURCE
    # ----------------------

    stop_words = [
    "في", "من", "على", "و", "الى", "إلى",
    "عن", "أن", "هذا", "هذه", "ذلك", "الذي",
    "التي", "كان", "كانت", "كما", "بين",
    "ولا", "لكن", "وقد", "لها", "له", "مع",
    "بعد", "قبل", "عند", "هناك", "أكثر",
    "أقل", "أحد", "أخرى", "أمام", "خلال",
    "حول", "ضمن", "حتى", "أو", "بل",
    "ثم", "أيضا", "جدا", "حيث", "حين",
    "إذا", "إن", "كل", "بعض", "جميع",
    "اليوم", "أمس", "غدا", "أبي",

    "الله", "غير", "آخر", "الثاني",
    "هسبريس", "هسبريس،",

    "ليس", "محمد", "الأخبار", "النشر"
]

    keywords_data = []

    # Loop through each source
    for source in df["source"].unique():

        # Articles from one source
        source_df = df[df["source"] == source]

        # Combine text
        all_text = " ".join(source_df["content"])

        # Split words
        words = all_text.split()

        # Clean words
        words = [
            w for w in words
            if w not in stop_words and len(w) > 2
        ]

        # Count frequency
        word_counts = Counter(words)

        # Top 10 keywords
        top_words = word_counts.most_common(10)

        # Save keywords with source
        for word, count in top_words:
            keywords_data.append({
                "word": word,
                "count": count,
                "source": source
            })

    # Create dataframe
    keywords_df = pd.DataFrame(keywords_data)

    # Save Gold CSV
    keywords_df.to_csv(
        "data/gold/top_keywords.csv",
        index=False
    )

    print("Top keywords created ✅")