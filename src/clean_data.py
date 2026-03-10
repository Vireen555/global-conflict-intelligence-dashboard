import os
import pandas as pd


INPUT_PATH = "data/raw/acled_events.csv"
OUTPUT_PATH = "data/processed/acled_events_cleaned.csv"


def clean_acled_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Convert date column to datetime
    df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce")

    # Convert numeric columns
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df["fatalities"] = pd.to_numeric(df["fatalities"], errors="coerce")

    # Drop rows without coordinates because map needs them
    df = df.dropna(subset=["latitude", "longitude"])

    # Fill text columns that may have missing values
    text_cols = [
        "actor1", "actor2", "admin1", "admin2", "location",
        "source", "notes", "sub_event_type", "event_type", "disorder_type"
    ]

    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    # Create extra useful columns
    df["fatalities"] = df["fatalities"].fillna(0)
    df["has_fatalities"] = df["fatalities"] > 0
    df["event_week"] = df["event_date"].dt.to_period("W").astype(str)
    df["event_month"] = df["event_date"].dt.to_period("M").astype(str)

    # Sort by date
    df = df.sort_values("event_date").reset_index(drop=True)

    return df


def main():
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"Input file not found: {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH)
    print("Raw shape:", df.shape)
    print("Raw columns:", df.columns.tolist())

    cleaned_df = clean_acled_data(df)

    os.makedirs("data/processed", exist_ok=True)
    cleaned_df.to_csv(OUTPUT_PATH, index=False)

    print("Cleaned shape:", cleaned_df.shape)
    print("Saved cleaned data to:", OUTPUT_PATH)
    print(cleaned_df.head())


if __name__ == "__main__":
    main()