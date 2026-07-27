import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BALLDONTLIE_API_KEY")
BASE_URL = "https://api.balldontlie.io/nba/v1"
HEADERS = {"Authorization": API_KEY}

# OKC's team ID must be looked up once via the /teams endpoint
def get_okc_team_id():
    resp = requests.get(f"{BASE_URL}/teams", headers=HEADERS)
    resp.raise_for_status()
    teams = resp.json()["data"]
    okc = next(t for t in teams if t["abbreviation"] == "OKC")
    return okc["id"]

def fetch_okc_games(season=2025):
    team_id = get_okc_team_id()
    games = []
    page = 1
    while True:
        resp = requests.get(
            f"{BASE_URL}/games",
            headers=HEADERS,
            params={"seasons[]": season, "team_ids[]": team_id, "per_page": 100, "page": page}
        )
        resp.raise_for_status()
        data = resp.json()
        games.extend(data["data"])
        if not data["meta"].get("next_cursor") and page >= data["meta"].get("total_pages", 1):
            break
        page += 1

    with open("ingestion/okc_2023_24_schedule.json", "w") as f:
        json.dump(games, f, indent=2)

    return games

if __name__ == "__main__":
    games = fetch_okc_games()
    print(f"Pulled {len(games)} games.")