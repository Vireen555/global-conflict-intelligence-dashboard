import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

ACLED_USERNAME = os.getenv("ACLED_USERNAME")
ACLED_PASSWORD = os.getenv("ACLED_PASSWORD")

TOKEN_URL = "https://acleddata.com/oauth/token"
DATA_URL = "https://acleddata.com/api/acled/read"


def get_access_token(username: str, password: str) -> str:
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "username": username,
        "password": password,
        "grant_type": "password",
        "client_id": "acled"
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)

    if response.status_code != 200:
        raise Exception(
            f"Failed to get access token: {response.status_code} {response.text}"
        )

    token_data = response.json()
    return token_data["access_token"]


def fetch_acled_data(access_token: str) -> pd.DataFrame:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    params = {
        "_format": "json",
        "event_date": "2026-01-01|2026-03-05",
        "event_date_where": "BETWEEN",
        "fields": (
            "event_id_cnty|event_date|year|disorder_type|event_type|sub_event_type|"
            "country|admin1|admin2|location|latitude|longitude|actor1|actor2|"
            "fatalities|source|notes"
        )
    }

    response = requests.get(DATA_URL, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch ACLED data: {response.status_code} {response.text}"
        )

    result = response.json()

    if result.get("status") != 200:
        raise Exception(f"API returned an error: {result}")

    data = result.get("data", [])
    return pd.DataFrame(data)


def main():
    if not ACLED_USERNAME or not ACLED_PASSWORD:
        raise ValueError("Missing ACLED_USERNAME or ACLED_PASSWORD in .env")

    print("Getting access token...")
    token = get_access_token(ACLED_USERNAME, ACLED_PASSWORD)
    print("Access token acquired successfully.")

    print("Fetching ACLED data...")
    df = fetch_acled_data(token)

    print("Data fetched successfully.")
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print(df.head())

    os.makedirs("data/raw", exist_ok=True)
    output_path = "data/raw/acled_events.csv"
    df.to_csv(output_path, index=False)
    print(f"Saved data to {output_path}")


if __name__ == "__main__":
    main()