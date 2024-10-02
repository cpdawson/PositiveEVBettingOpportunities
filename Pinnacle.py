import pandas as pd
import requests

url = 'https://api.the-odds-api.com/v4/sports/baseball_mlb/odds/?regions=eu&markets=h2h&oddsFormat=decimal&apiKey=ccae58c1e160f0d2c74eb48a8720c271'

response = requests.get(url)
data = response.json()

flattened_data = []

for item in data:
    for bookmaker in item['bookmakers']:
        if bookmaker['key'] == 'pinnacle':
            for market in bookmaker['markets']:
                for outcome in market['outcomes']:
                    flattened_data.append({
                        'id': item['id'],
                        'sport_key': item['sport_key'],
                        'sport_title': item['sport_title'],
                        'commence_time': item['commence_time'],
                        'home_team': item['home_team'],
                        'away_team': item['away_team'],
                        'bookmaker_key': bookmaker['key'],
                        'bookmaker_title': bookmaker['title'],
                        'market_key': market['key'],
                        'outcome_name': outcome['name'],
                        'outcome_price': outcome['price'],
                        'point': outcome['point'] if 'point' in outcome else None
                    })

df_final = pd.DataFrame(flattened_data)

# Write to Excel
df_final.to_excel('pinnacle_odds.xlsx', index=False)
