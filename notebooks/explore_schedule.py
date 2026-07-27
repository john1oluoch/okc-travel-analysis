import json
import pandas as pd

with open("ingestion/okc_2023_24_schedule.json") as f:
    games = json.load(f)

df = pd.json_normalize(games)  # flattens nested dicts (home_team, visitor_team, etc.)

print("Shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nFirst 5 rows:\n", df.head())

# Check 1: row count
print("\n--- Check 1: Row count ---")
print("Total games:", df.shape[0])

# Check 2: confirm every row involves OKC
print("\n--- Check 2: OKC presence in every row ---")
is_okc_home = df["home_team.abbreviation"] == "OKC"
is_okc_away = df["visitor_team.abbreviation"] == "OKC"
non_okc_rows = df[~(is_okc_home | is_okc_away)]
print("Rows with neither team as OKC:", len(non_okc_rows))
if len(non_okc_rows) > 0:
    print(non_okc_rows[["home_team.abbreviation", "visitor_team.abbreviation"]])

# Check 3: null/missing dates
print("\n--- Check 3: Null dates ---")
print("Null date count:", df["date"].isna().sum())
print("Sample dates:", df["date"].head(3).tolist())