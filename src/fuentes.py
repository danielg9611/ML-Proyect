import requests
from datetime import date


import pandas as pd
import numpy as np

url = "https://v3.football.api-sports.io/fixtures"
headers = {
    "x-apisports-key": "318d0a987867780f845c84150129d9a7"
}
params = {
    "date": date.today().strftime("%Y-%m-%d"),
    "status": "NS",
    "league": 140
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

# Print match info
for fixture in data["response"]:
    print(f"{fixture['teams']['home']['name']} vs {fixture['teams']['away']['name']} at {fixture['fixture']['date']}")




def get_fixtures(season):
    url = "https://v3.football.api-sports.io/fixtures"
    params = {
        "league": 140,       # La Liga
        "season": season     # 2023 or 2022
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()["response"]


fixtures_2021 = get_fixtures(2021)
fixtures_2022 = get_fixtures(2022)
fixtures_2023 = get_fixtures(2023)

# print(f"2023 season matches: {len(fixtures_2023)}")
# print(fixtures_2021)
# print(fixtures_2022)

# print(f"2022 season matches: {len(fixtures_2022)}")


all_fixtures = fixtures_2021 + fixtures_2022 + fixtures_2023



data = []
for fixture in all_fixtures:
    data.append({
        "fixture_id": fixture["fixture"]["id"],
        "date": fixture["fixture"]["date"],

        "home_team": fixture["teams"]["home"]["name"],
        "home_team_id": fixture["teams"]["home"]["id"],
        "away_team": fixture["teams"]["away"]["name"],
        "away_team_id": fixture["teams"]["away"]["id"],
        "home_score": fixture["goals"]["home"],
        "away_score": fixture["goals"]["away"],
        "home_winner": fixture["teams"]["home"]["winner"],
        "away_winner": fixture["teams"]["away"]["winner"],

        "league_season": fixture["league"]["season"]
    })

df = pd.DataFrame(data)


df['date'] = pd.to_datetime(df['date'])



df['home_result'] = np.where(df['home_winner'] == True,'WIN','DRAW')
df['home_result'] = np.where(df['home_winner'] == False,'LOSS',df['home_result'])



df.set_index('fixture_id', inplace=True)


df.to_csv('../data/raw/dataset.csv')