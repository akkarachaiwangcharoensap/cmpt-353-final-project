import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from understatapi import UnderstatClient

# Function to load data from JSON or fetch from API
def load_or_fetch_data(json_path, league, season):
    if os.path.exists(json_path):
        print(f"Loading data from {json_path}...")
        return pd.read_json(json_path).to_dict()
    else:
        with UnderstatClient() as understat:
            print(f"Fetching data for {league} {season} season...")
            data = understat.league(league=league).get_team_data(season=season)
            
            # Save data to JSON
            with open(json_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            print(f"Data saved to {json_path}.")

            return data
        
def load_or_fetch_players_data(json_path, league, season):
    if os.path.exists(json_path):
        print(f"Loading data from {json_path}...")
        return pd.read_json(json_path)
    else:
        with UnderstatClient() as understat:
            print(f"Fetching player data for {league} {season} season...")
            # Fetch player data for the league and season
            data = understat.league(league=league).get_player_data(season=season)
            
            # Save data to JSON
            with open(json_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            print(f"Player data saved to {json_path}.")
            
            return data

def get_teams(json_data):
    # Flatten the JSON structure into a list of records
    records = [
        {**{'team': team_data['title']}, **history_item}
        for team_data in json_data.values()
        for history_item in team_data['history']
    ]
    
    # Grab the following columns
    cols = ['team', 'h_a', 'xG', 'xGA', 'scored', 'wins', 'draws', 'loses', 'result', 'date']
    
    # Convert the list of records to a DataFrame
    final_df = pd.DataFrame(records)[cols]
    return final_df

def get_players(json_data):
    df = pd.DataFrame(json_data)
    
    # Select specified columns
    selected_columns = [
        'id', 'player_name', 'games', 'time', 'goals', 'xG', 
        'assists', 'xA', 'team_title'
    ]
    return df[selected_columns]

def plot_home_vs_away_wins(home_data, away_data, league='EPL', period = ''):
    # Merge home and away aggregated data for comparison
    comparison_data = home_data.merge(
        away_data, on="team", suffixes=('_home', '_away')
    )

    # Scatterplot for wins comparison
    plt.figure(figsize=(10, 6))
    plt.scatter(comparison_data['wins_sum_home'], comparison_data['wins_sum_away'], alpha=0.7, color='blue')
    for i, team in enumerate(comparison_data['team']):
        plt.text(
            comparison_data['wins_sum_home'][i],
            comparison_data['wins_sum_away'][i],
            team,
            fontsize=8,
            ha='right'
        )

    # Ensure ticks show only whole integers
    max_home_wins = comparison_data['wins_sum_home'].max()
    max_away_wins = comparison_data['wins_sum_away'].max()
    plt.xticks(range(0, max_home_wins + 1))
    plt.yticks(range(0, max_away_wins + 1))

    # Add plot details
    plt.title(f"Home vs Away Wins ({league} {period})")
    plt.xlabel('Home Wins')
    plt.ylabel('Away Wins')
    plt.axline((0, 0), slope=1, color='red', linestyle='--', linewidth=1)
    plt.tight_layout()
    plt.show()

def plot_home_vs_away_scores(home_data, away_data, league='EPL', period=''):
    # Merge home and away aggregated data for comparison
    comparison_data = home_data.merge(
        away_data, on="team", suffixes=('_home', '_away')
    )

    # Scatterplot for wins comparison
    plt.figure(figsize=(14, 8))
    plt.scatter(comparison_data['xG_sum_home'], comparison_data['xG_sum_away'], alpha=0.7, color='blue')
    for i, team in enumerate(comparison_data['team']):
        plt.text(
            comparison_data['xG_sum_home'][i],
            comparison_data['xG_sum_away'][i],
            team,
            fontsize=8,
            ha='right'
        )

    # Ensure ticks show only whole integers
    max_home_scores = comparison_data['xG_sum_home'].max()
    max_away_scores = comparison_data['xG_sum_away'].max()
    plt.xticks(range(0, max_home_scores + 2))
    plt.yticks(range(0, max_away_scores + 2))

    # Add plot details
    plt.title(f"Home vs Away Scores ({league} {period})")
    plt.xlabel('Home Scores')
    plt.ylabel('Away Scores')
    plt.axline((0, 0), slope=1, color='red', linestyle='--', linewidth=1)
    plt.tight_layout()
    plt.show()

def plot_home_vs_away_xg(home_data, away_data, league='EPL', period=''):
    # Merge home and away aggregated xG data for comparison
    comparison_data = home_data.merge(
        away_data, on="team", suffixes=('_home', '_away')
    )

    # Scatterplot for xG comparison
    plt.figure(figsize=(14, 8))
    plt.scatter(comparison_data['xG_sum_home'], comparison_data['xG_sum_away'], alpha=0.7, color='green')
    for i, team in enumerate(comparison_data['team']):
        plt.text(
            comparison_data['xG_sum_home'][i],
            comparison_data['xG_sum_away'][i],
            team,
            fontsize=8,
            ha='right'
        )

    # Ensure ticks show only whole integers
    max_home_xg = comparison_data['xG_sum_home'].max()
    max_away_xg = comparison_data['xG_sum_away'].max()
    plt.xticks(range(0, int(max_home_xg) + 2))
    plt.yticks(range(0, int(max_away_xg) + 2))

    # Add plot details
    plt.title(f"Home vs Away xG Scores ({league} {period})")
    plt.xlabel('Home xG Scores')
    plt.ylabel('Away xG Scores')
    plt.axline((0, 0), slope=1, color='red', linestyle='--', linewidth=1)
    plt.tight_layout()
    plt.show()