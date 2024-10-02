import main
import Pinnacle

import pandas as pd

# Read both Excel files
df_max_prices = pd.read_excel('max_prices.xlsx')
df_pinnacle_odds = pd.read_excel('pinnacle_odds.xlsx')
offshore_books = ['Fliff']

# List to store positive EV bets
positive_ev_bets = []

# Iterate through unique game IDs
unique_game_ids = df_max_prices['id'].unique()

for game_id in unique_game_ids:
    max_prices_game = df_max_prices[df_max_prices['id'] == game_id]
    pinnacle_odds_game = df_pinnacle_odds[df_pinnacle_odds['id'] == game_id]

    for index, max_price_row in max_prices_game.iterrows():
        team_name = max_price_row['outcome_name']
        max_price = max_price_row['outcome_price']
        sportsbook = max_price_row['bookmaker_title']

        # Check if there is a corresponding row for the team in pinnacle_odds_game
        pinnacle_price_rows = pinnacle_odds_game[pinnacle_odds_game['outcome_name'] == team_name]
        if pinnacle_price_rows.empty:
            print(f"No Pinnacle odds found for {team_name} in game {game_id}. Skipping.")
            continue

        pinnacle_price_row = pinnacle_price_rows.iloc[0]
        pinnacle_price = pinnacle_price_row['outcome_price']

        # The rest of the code as before
        # ...


        # Compare the odds and store positive EV bets
        if max_price > pinnacle_price:
            bet = {
                'game_id': game_id,
                'team_name': team_name,
                'max_price': max_price,
                'pinnacle_price': pinnacle_price,
                'sportsbook': sportsbook # Store the sportsbook name
            }
            positive_ev_bets.append(bet)
            if sportsbook in offshore_books:
                print(f"Better odds for {team_name} in game {game_id} at {sportsbook}: {max_price} vs Pinnacle's {pinnacle_price}")

# Now, positive_ev_bets is a list of dictionaries, each representing a positive EV bet
