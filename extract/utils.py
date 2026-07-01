import json
from pathlib import Path

import requests

BASE_URL = "https://dummyjson.com"
RAW_DATA_DIR = Path("data/raw")


def fetch_data(endpoint):
    url = f"{BASE_URL}{endpoint}"

    response = requests.get(url)
    response.raise_for_status()

    return response.json()


def save_json(data, filename):
    """
    Save API response as a JSON file in the raw data directory.
    """
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    file_path = RAW_DATA_DIR / filename

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print(f"Saved: {file_path}")


