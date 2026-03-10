import os
import time
import requests
import pandas as pd

GDELT_DOC_URL = "https://api.gdeltproject.org/api/v2/doc/doc"


def fetch_gdelt_articles(
    query: str = '("war" OR "conflict" OR "airstrike" OR "ceasefire")',
    timespan: str = "10d",
    maxrecords: int = 200,
    max_retries: int = 5,
    retry_wait: int = 6,
) -> pd.DataFrame:
    params = {
        "query": query,
        "mode": "artlist",
        "format": "json",
        "sort": "datedesc",
        "timespan": timespan,
        "maxrecords": maxrecords,
    }

    for attempt in range(1, max_retries + 1):
        print(f"Attempt {attempt} of {max_retries}...")
        response = requests.get(GDELT_DOC_URL, params=params, timeout=60)

        print("Request URL:", response.url)
        print("Status code:", response.status_code)

        # Handle rate limiting
        if response.status_code == 429:
            print(f"Rate limited by GDELT. Waiting {retry_wait} seconds before retrying...")
            time.sleep(retry_wait)
            continue

        if response.status_code != 200:
            raise Exception(
                f"GDELT request failed: {response.status_code}\n"
                f"Response preview: {response.text[:500]}"
            )

        # Try JSON safely
        try:
            data = response.json()
        except Exception:
            print("Response was not valid JSON.")
            print("Raw response preview:")
            print(response.text[:1000])
            raise

        articles = data.get("articles", [])

        if not articles:
            print("No articles returned.")
            print("Raw response preview:")
            print(str(data)[:1000])
            return pd.DataFrame()

        return pd.DataFrame(articles)

    raise Exception("GDELT request kept getting rate-limited after multiple retries.")


def main():
    df = fetch_gdelt_articles(
        query='(war OR conflict OR airstrike OR ceasefire)',
        timespan="10d",
        maxrecords=200,
        max_retries=5,
        retry_wait=6,
    )

    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print(df.head())

    os.makedirs("data/raw", exist_ok=True)
    output_path = "data/raw/gdelt_war_news.csv"
    df.to_csv(output_path, index=False)
    print(f"Saved data to {output_path}")


if __name__ == "__main__":
    main()
