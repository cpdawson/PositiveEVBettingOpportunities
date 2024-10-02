import pandas as pd
import requests
american_sports = ['baseball_mlb', 'soccer_usa_mls', 'icehockey_nhl', 'americanfootball_ncaaf', 'americanfootball_nfl', 'basketball_nba']

# URL for your data
url = 'https://api.the-odds-api.com/v4/sports/baseball_mlb/odds/?regions=us&markets=h2h&oddsFormat=decimal&apiKey=ccae58c1e160f0d2c74eb48a8720c271'

# Fetch the data from the URL
response = requests.get(url)
data = response.json()

# Creating a list to hold the flattened data
flattened_data = []

# Looping through the data to flatten it
for item in data:
    for bookmaker in item['bookmakers']:
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
                    'outcome_price': outcome['price']
                })

# Convert the flattened data to a DataFrame
df_final = pd.DataFrame(flattened_data)

# Find the index of the row with the highest outcome_price for each group (id and outcome_name)
idx = df_final.groupby(['id', 'outcome_name'])['outcome_price'].idxmax()

# Select the rows with the highest outcome_price for each group
df_max_prices = df_final.loc[idx]

# Write to Excel
df_max_prices.to_excel('max_prices.xlsx', index=False)
