import os
import pandas as pd


INPUT_PATH = "data/raw/gdelt_war_news.csv"
OUTPUT_PATH = "data/processed/gdelt_war_news_cleaned.csv"


KEYWORD_GROUPS = {
    "Ukraine": ["ukraine", "kyiv", "zelensky", "russia", "putin", "donbas"],
    "Middle East": ["israel", "gaza", "hamas", "iran", "lebanon", "hezbollah", "middle east", "west asia"],
    "Sudan": ["sudan", "khartoum", "rsf", "darfur"],
    "Myanmar": ["myanmar", "burma", "junta"],
}

INCLUDE_KEYWORDS = [
    "war", "conflict", "airstrike", "ceasefire", "missile", "attack",
    "invasion", "military", "drone", "strike", "shelling", "troops",
    "hamas", "gaza", "iran", "israel", "ukraine", "russia", "sudan",
    "myanmar", "lebanon", "hezbollah", "west asia", "middle east"
]

EXCLUDE_KEYWORDS = [
    "movie", "film", "trailer", "review", "box office", "series",
    "episode", "teases", "game", "gaming", "fantasy", "calamity",
    "comic", "marvel", "dc", "netflix", "anime", "celebrity",
    "song", "album", "tv show"
]


def normalize_text(text: str) -> str:
    if pd.isna(text):
        return ""
    return str(text).strip()


def detect_conflict_topic(title: str) -> str:
    title_lower = normalize_text(title).lower()

    for topic, keywords in KEYWORD_GROUPS.items():
        if any(keyword in title_lower for keyword in keywords):
            return topic

    return "Other"


def is_conflict_relevant(title: str) -> bool:
    title_lower = normalize_text(title).lower()

    has_include = any(keyword in title_lower for keyword in INCLUDE_KEYWORDS)
    has_exclude = any(keyword in title_lower for keyword in EXCLUDE_KEYWORDS)

    return has_include and not has_exclude


def extract_domain_category(domain: str) -> str:
    domain = normalize_text(domain).lower()

    if not domain:
        return "Unknown"
    if domain.endswith(".gov") or ".gov." in domain:
        return "Government"
    if domain.endswith(".mil") or ".mil." in domain:
        return "Military"
    if domain.endswith(".org"):
        return "Organization"
    return "News/Media"


def clean_gdelt_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    desired_columns = [
        "title",
        "seendate",
        "domain",
        "language",
        "sourcecountry",
        "url",
        "socialimage",
        "url_mobile",
    ]
    existing_columns = [col for col in desired_columns if col in df.columns]
    df = df[existing_columns]

    for col in ["title", "domain", "language", "sourcecountry", "url", "socialimage", "url_mobile"]:
        if col in df.columns:
            df[col] = df[col].apply(normalize_text)

    df = df[df["title"].str.len() > 0]

    subset_cols = [col for col in ["title", "url"] if col in df.columns]
    if subset_cols:
        df = df.drop_duplicates(subset=subset_cols)

    if "seendate" in df.columns:
        df["seendate"] = pd.to_datetime(df["seendate"], format="%Y%m%dT%H%M%SZ", errors="coerce")
        df = df.dropna(subset=["seendate"])

    df["is_conflict_relevant"] = df["title"].apply(is_conflict_relevant)
    df = df[df["is_conflict_relevant"]].copy()

    df["conflict_topic"] = df["title"].apply(detect_conflict_topic)
    df["domain_category"] = df["domain"].apply(extract_domain_category)

    df["publish_date"] = df["seendate"].dt.date
    df["publish_hour"] = df["seendate"].dt.hour
    df["publish_day"] = df["seendate"].dt.day_name()

    for col in ["language", "sourcecountry", "domain", "domain_category", "conflict_topic"]:
        if col in df.columns:
            df[col] = df[col].replace("", "Unknown").fillna("Unknown")

    df = df.sort_values("seendate", ascending=False).reset_index(drop=True)
    return df


def main():
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"Input file not found: {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH)
    print("Raw shape:", df.shape)
    print("Raw columns:", df.columns.tolist())

    cleaned_df = clean_gdelt_data(df)

    os.makedirs("data/processed", exist_ok=True)
    cleaned_df.to_csv(OUTPUT_PATH, index=False)

    print("Cleaned shape:", cleaned_df.shape)
    print("Cleaned columns:", cleaned_df.columns.tolist())
    print(cleaned_df.head())

    if "conflict_topic" in cleaned_df.columns:
        print("\nConflict topic counts:")
        print(cleaned_df["conflict_topic"].value_counts())

    if "sourcecountry" in cleaned_df.columns:
        print("\nTop source countries:")
        print(cleaned_df["sourcecountry"].value_counts().head(10))


if __name__ == "__main__":
    main()