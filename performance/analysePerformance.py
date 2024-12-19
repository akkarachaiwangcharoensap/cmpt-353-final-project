'''Program to dive deeper into the offensive and defensive data of teams. 
This will run statistical tests on both offensive and defensive metrics, 
including saves, blocked shots, total tackles, interceptions, clearances, 
total shots, corners won, possession percentage, and crosses.
This will also analyse any potential referee biases, by analysing metrics such
as fouls, yellow cards, and red cards.
'''

import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, mannwhitneyu, normaltest, levene
import numpy as np
import os

# Mapping of column names to readable forms for streamlined visual plotting
COLUMN_NAME_MAPPING = {
    'total_shots': 'Total Shots',
    'won_corners': 'Corners Won',
    'possession_pct': 'Possession (%)',
    'total_crosses': 'Total Crosses',
    'fouls_committed': 'Fouls Committed',
    'saves': 'Saves',
    'blocked_shots': 'Blocked Shots',
    'total_tackles': 'Total Tackles',
    'interceptions': 'Interceptions',
    'total_clearance': 'Clearances',
    'yellow_cards' : 'Yellow Cards',
    'red_cards' : 'Red Cards'
}

# Function to try transforming data in multiple ways and see if any transformations pass normal test
def transform_data(data, col_name):
    transformations = {
        'original': data[col_name],
        'square_root': np.sqrt(data[col_name]),
        'log': np.log1p(data[col_name]),# log1p handles zeroes gracefully
        'square': np.power(data[col_name], 2),# Squaring transformation
        'exponential': np.exp(data[col_name] / data[col_name].max()),# Exponential transformation
    }
    return transformations

# Function to return a bool value if the data passed normal test
def check_normality(data, col_name):
    stat, p_value = normaltest(data[col_name])
    print(f"{col_name} Normal Test: p = {p_value}")
    return p_value > 0.05  # p-value > 0.05 indicates normality

# Function to return a bool value if the data passed equivariance test
def check_equal_variance(home_data, away_data, col_name):
    stat, p_value = levene(home_data[col_name], away_data[col_name])
    return p_value > 0.05  # p-value > 0.05 indicates equal variance

# Helper function to ensure there exists a directory for the plots
def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

'''Function to handle the statistical analysis of home and away data passed in. 
    Begins with checking for normality, if this fails then will apply a transformation function
    that returns a list of various transformations. It then iterates through these transformations,
    and checks for normality for each. Then proceeds to the appropriate statistical test'''
def run_statistical_tests(home_data, away_data, col_name):
    print(f"\nAnalyzing {col_name}:")

    # Check normality and equal variance
    home_normal = check_normality(home_data, col_name)
    away_normal = check_normality(away_data, col_name)
    equal_variance = check_equal_variance(home_data, away_data, col_name)

    print(f"Home normality test: {'Pass' if home_normal else 'Fail'}")
    print(f"Away normality test: {'Pass' if away_normal else 'Fail'}")
    print(f"Equal variance test: {'Pass' if equal_variance else 'Fail'}")

    # Attempt transformations if data is not normal
    if not home_normal or not away_normal:
        print("Data is not normal. Attempting transformations...")
        transformations_home = transform_data(home_data, col_name)
        transformations_away = transform_data(away_data, col_name)

    # Apply transformations to each dataset
    for name, transformed_home_data in transformations_home.items():
        transformed_away_data = transformations_away.get(name, None)  # Ensure corresponding transformation exists for away data

        if transformed_away_data is not None:
            home_data[name] = transformed_home_data
            away_data[name] = transformed_away_data

    # Re-check normality after transformations
    for transformation_name in transformations_home.keys():
        home_normal = check_normality(home_data, transformation_name)
        away_normal = check_normality(away_data, transformation_name)
        if home_normal and away_normal:
            print(f"Data became normal after {transformation_name} transformation.")
            col_name = transformation_name  # Use the transformed data for testing
            break
    else:
        print("Data could not be transformed to normality.")

    # Perform statistical test
    if home_normal and away_normal:
        print("Using T-Test (normal data)...")
        stat, p_value = ttest_ind(home_data[col_name], away_data[col_name], equal_var=equal_variance)
    else:
        print("Using Mann-Whitney U Test (non-normal data)...")
        stat, p_value = mannwhitneyu(home_data[col_name], away_data[col_name])

    # Report results
    print(f"Test statistic: {stat}, p-value: {p_value}")
    if p_value < 0.05:
        print(f"Significant evidence to suggest a difference home vs away for {col_name}.")
    else:
        print(f"No significant evidence to suggest a difference home vs away for {col_name}.")

# Helper aggregate functions, one that takes mean values only by team name, and one that does season and team name
def aggregate_team_performance(home_data, away_data, col_name):
    home_agg = home_data.groupby('team_name')[col_name].mean().reset_index()
    away_agg = away_data.groupby('team_name')[col_name].mean().reset_index()

    # Merge the aggregated data on team_name
    team_performance = pd.merge(home_agg, away_agg, on=['team_name'], suffixes=('_home', '_away'))
    return team_performance

def aggregate_team_performance_by_season(home_data, away_data, col_name):
    home_agg = home_data.groupby(['team_name', 'season'])[col_name].mean().reset_index()
    away_agg = away_data.groupby(['team_name', 'season'])[col_name].mean().reset_index()

    # Merge the aggregated data on team_name
    team_performance = pd.merge(home_agg, away_agg, on=['team_name', 'season'], suffixes=('_home', '_away'))
    return team_performance

def plot_histograms(home_data, away_data, col_name):
    # Get readable column name
    readable_col_name = COLUMN_NAME_MAPPING.get(col_name, col_name)
    # To ensure correct directory
    histogram_dir = "performancePlots/histograms"
    ensure_directory(histogram_dir)
    
    plt.figure(figsize=(10, 6))
    sns.histplot(home_data[col_name], color="blue", label="Home", kde=True, alpha=0.6, bins=20)
    sns.histplot(away_data[col_name], color="orange", label="Away", kde=True, alpha=0.6, bins=20)
    plt.title(f"Histogram of {readable_col_name}: Home vs Away 2015 - 2021", fontsize=14)
    plt.xlabel(readable_col_name, fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(histogram_dir, f"{col_name}_histogram.png"))
    plt.close()


def plot_scatterplot(team_performance, col_name):
    readable_col_name = COLUMN_NAME_MAPPING.get(col_name, col_name)
    # To ensure correct directory
    scatterplot_dir = "performancePlots/scatterplots"
    ensure_directory(scatterplot_dir)
    
    plt.figure(figsize=(10, 6))
    plt.scatter(team_performance[f"{col_name}_home"], team_performance[f"{col_name}_away"],
                color="green", alpha=0.7)

    max_val = max(team_performance[f"{col_name}_home"].max(), team_performance[f"{col_name}_away"].max())
    plt.plot([0, max_val], [0, max_val], linestyle="--", color="red", alpha=0.5)

    for _, row in team_performance.iterrows():
        plt.text(row[f"{col_name}_home"], row[f"{col_name}_away"], row["team_name"],
                 fontsize=9, ha="right", va="bottom")

    plt.title(f"Home vs Away {readable_col_name} by Team 2015-2021", fontsize=14)
    plt.xlabel(f"Home {readable_col_name}", fontsize=12)
    plt.ylabel(f"Away {readable_col_name}", fontsize=12)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(scatterplot_dir, f"{col_name}_scatterplot.png"))
    plt.close()

    
def plot_stacked_bar_chart(home_data, away_data, col_name):
    readable_col_name = COLUMN_NAME_MAPPING.get(col_name, col_name)
    
    # To ensure correct directory
    stacked_dir = "performancePlots/stackedBarPlot"
    ensure_directory(stacked_dir)

    home_agg = home_data.groupby('team_name')[col_name].sum().reset_index()
    away_agg = away_data.groupby('team_name')[col_name].sum().reset_index()
    combined = pd.merge(home_agg, away_agg, on='team_name', suffixes=('_home', '_away'))

    combined.set_index('team_name', inplace=True)
    combined = combined.sort_values(by=f"{col_name}_home", ascending=False)

    combined.plot(kind='bar', stacked=True, figsize=(12, 8), color=["blue", "orange"])
    plt.title(f"Cumulative {readable_col_name} by Team: Home vs Away", fontsize=14)
    plt.xlabel("Team", fontsize=12)
    plt.ylabel(readable_col_name, fontsize=12)
    plt.legend(["Home", "Away"], fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(stacked_dir, f"{col_name}_stacked_barplot.png"))
    plt.close()

def plot_boxplot(home_data, away_data, col_name):
    readable_col_name = COLUMN_NAME_MAPPING.get(col_name, col_name)
    
    # To ensure correct directory
    boxplot_dir = "performancePlots/boxPlots"
    ensure_directory(boxplot_dir)

    # Combine home and away data with labels
    home_data['Location'] = 'Home'
    away_data['Location'] = 'Away'
    combined_data = pd.concat([home_data[[col_name, 'Location']], away_data[[col_name, 'Location']]])

    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Location', y=col_name, data=combined_data, palette='Set2')
    plt.title(f"Boxplot of {readable_col_name}: Home vs Away", fontsize=14)
    plt.xlabel("Location", fontsize=12)
    plt.ylabel(readable_col_name, fontsize=12)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(boxplot_dir, f"{col_name}_boxplot.png"))
    plt.close()
    
# Function to analyse every column of the dataframe.
def analyse_column(data, col_name):
    home_data = data[data['is_home'] == True].copy()
    away_data = data[data['is_home'] == False].copy()

    home_data['team_name'] = home_data['home_team']
    away_data['team_name'] = away_data['away_team']

    home_data = home_data.drop(columns=['home_team', 'away_team'])
    away_data = away_data.drop(columns=['home_team', 'away_team'])

    team_performance = aggregate_team_performance(home_data, away_data, col_name)
    
    '''
        Below are functions to be called to create various plots with the data.
        These are commented out for easy running of just the stats tests, but feel
        free to uncomment any plot. These are all being saved in
        /plots.
    '''

    #plot_histograms(home_data, away_data, col_name)
    #plot_scatterplot(team_performance, col_name)
    #plot_stacked_bar_chart(home_data, away_data, col_name)
    #plot_boxplot(home_data, away_data, col_name)

    # Call the stat test helper function
    run_statistical_tests(home_data, away_data, col_name)


def main():
    if len(sys.argv) < 2:
        print("Usage: python program.py <csv_file1> <csv_file2> ...")
        sys.exit(1)

    # Get the directory from the command-line arguments
    directory = sys.argv[1]

    # Verify that the provided path is a directory
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        sys.exit(1)

    # Get all CSV files in the directory
    csv_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.csv')]

    if not csv_files:
        print("No CSV files found in the directory.")
        sys.exit(1)
    
    # Initialize an empty dataframe
    data = None

    # Read and append each CSV file
    for csv_file in csv_files:
        try:
            print(f"Reading {csv_file}...")
            temp_data = pd.read_csv(csv_file)
            data = pd.concat([data, temp_data], ignore_index=True)
        except Exception as e:
            print(f"Error reading {csv_file}: {e}")
            sys.exit(1)

    print(f"Combined dataframe shape: {data.shape}")

    # Define offensive and defensive columns
    offensive_cols = ['total_shots', 'won_corners', 'possession_pct', 'total_crosses', 'fouls_committed', 'yellow_cards', 'red_cards']
    defensive_cols = ['saves', 'blocked_shots', 'total_tackles', 'interceptions', 'total_clearance']

    # Analyse each column
    for col in offensive_cols + defensive_cols:
        if col in data.columns:  # Only analyse if the column exists in the dataframe
            print(f"\nAnalyzing {col}...")
            analyse_column(data, col)
        else:
            print(f"Column {col} not found in the combined data. Skipping...")



if __name__ == "__main__":
    main()
