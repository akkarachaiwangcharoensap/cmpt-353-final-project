# CMPT353-FinalProject
Final Project for the MoneyBall Group for SFU's FALL 2024 CMPT 353 class

## Project Structure (to be updated)
```bash
repository
├── covid-19
│   ├── src
│   │   ├── utility.py
│   ├── analyze_teams.ipynb
│   ├── epl_overall_players_performance.ipynb
│   ├── epl_players_data_2014_2015.json
│   ├── epl_players_data_2015_2016.json
│   ├── epl_players_data_2016_2017.json
│   ├── epl_players_data_2017_2018.json
│   ├── epl_players_data_2018_2019.json
│   ├── epl_players_data_2019_2020.json
│   ├── epl_players_data_2020_2021.json
│   ├── epl_players_data_2021_2022.json
│   ├── epl_players_data_2022_2023.json
│   ├── epl_players_data_2023_2024.json
│   ├── epl_team_data_2020_2021.json
│   ├── epl_teams_data_2019_2020.json
├── data
│   ├── 2020
│   │   ├── Bundesliga-2020.csv
│   │   ├── EPL-2020.csv
│   │   ├── La_Liga-2020.csv
│   │   ├── ...
│   ├── 2023
│   │   ├── Bundesliga-2023.csv
│   │   ├── EPL-2023.csv
│   │   ├── La_Liga-2023.csv
│   │   ├── ...
│   ├── Bundesliga_2020
│   │   ├── pvalue
│   │   │   ├── Bundesliga_2020_with_pvalue.csv
│   │   ├── Arminia_Bielefeld_Matches_2020.csv
│   │   ├── Augsburg_Matches_2020.csv
│   │   ├── ...
│   ├── Bundesliga_2023
│   │   ├── pvalue
│   │   │   ├── Bundesliga_2023_with_pvalue.csv
│   │   ├── Augsburg_Matches_2023.csv
│   │   ├── Bayer_Leverkusen_Matches_2023.csv
│   │   ├── ...
│   ├── EPL_2020
│   │   ├── pvalue
│   │   │   ├── EPL_2020_with_pvalues.csv
│   │   ├── Arsenal_Matches_2020.csv
│   │   ├── Aston_Villa_Matches_2020.csv
│   │   ├── ...
│   ├── ...
├── graphs
│   ├── scatterplots
│   │   ├── Bundesliga
│   │   │   ├── Bundesliga_2020_scatterplots.png
│   │   │   ├── ...
│   │   ├── EPL
│   │   │   ├── EPL_2020_scatterplots.png
│   │   │   ├── ...
│   │   ├── ...
├── performance
│   ├── performanceData
│   │   ├── EPL_2015_matchsheets.csv
│   │   ├── ...
│   ├── performancePlots
│   │   ├── boxPlots
│   │   ├── histograms
│   │   ├── scatterplots
│   │   ├── stackedBarPlots
│   ├── analysePerformance.py
│   ├── gatherPerformanceData.ipynb
├── analyseData.py
├── cleanData.py
├── dataBoxplot.py
├── dataHistogram.py
├── gatherData.py
├── leagueDataBoxPlot.py
├── leagueDataHistogram.py
├── leagueDataScatter.py
```

## Libraries required

understatapi 

soccerdata

pandas

numpy

scipy

matplotlib

seaborn

If any of these librarys are not yet installed:
```bash
pip install <library>
```

## Getting Started with Initial data
Please proceed in the following order

### i)`gatherData.py`
Gathers data from understatapi to reformat and prep for `cleanData.py`, exports as `<league>-<year>.csv` in `data/<year>`
to run, enter in terminal:
```bash
python3 gatherData.py <year>
```

### ii)`cleanData.py`
Uses data from `gatherData.py` as well as match data to create annual match data(match id,side,result,goals_for,goals_against,xG_for,xG_against) for each team and exports it as a csv file in `data/<league>_<year>/` nammed `<team>_<year>.csv` in every league.
to run, enter in terminal:
```bash
python3 cleanData.py <year>
```
Both This program and ` gatherData.py` will take a bit to gather so we already included the nessesary data for 2020 and 2023 as sample data so you can just start from `analyzeData.py`

### iii)`analyzeData.py`
Conducts t-test across every metric from the `cleanData.py` export for every team in every league, exports all the pvalues as well as the home vs away value for each metric in a csv, sorted by total points. Exports as `<league>_<year>_with_pvalues.csv` in `/data/<league>__<year>/pvalue/`
to run, enter in terminal:
```bash
python3 analyzeData.py <year>
```

## Visualising initial Data

### League Data
Creates a graph for each p-value created from `analyzeData.py` and places every team in comparison to each other across the league.
All of these programs export graphs of different metrics for across the league for the top 5 leagues in a specified year.
### i)`leagueDataScatter.py`
to run, enter in terminal:
```bash
python3 leagueDataScatter.py <year>
```

### ii)`leagueDataBoxPlot.py`
to run, enter in terminal:
```bash
python3 leagueDataBoxPlot.py <year>
```

### iii)`leagueDataHistogram.py`
to run, enter in terminal:
```bash
python3 leagueDataHistogram.py <year>
```

### Team Data
Creates a graph for each p-value created from `analyzeData.py` for each team.
All of these programs export graphs of different metrics for each team in the specified league/year.
the list of leagues that can be run are "EPL", "La_Liga", "Bundesliga", "Ligue_1", and "Serie_A" 
### i)`dataBoxplot.py`
to run, enter in terminal:
```bash
python3 leagueDataScatter.py <league> <year>
```

### ii)`dataBoxplot.py`
to run, enter in terminal:
```bash
python3 dataBoxplot.py <league> <year>
```

## Europe Premier League (EPL) During COVID-19

### `analyze_teams.ipynb`
Analyzes and compares Expected Goals (xG) statistics for football matches, focusing on home versus away performances for a EPL league during COVID-19 seasons. The analysis separates matches into home and away categories, visualizing xG distributions using histograms and generating comparative plots.

### `epl_overall_players_performance.ipynb`
Analyzes and compares Expected Goals (xG) statistics for all football players across multiple seasons in the English Premier League, focusing on differences between COVID-affected seasons (2019–2020 and 2020–2021) and pre-and-post-COVID seasons (2014–2019 and 2021–2023). In statistical anaylsis, we used T-test or Mann-Whitney U to determine if xG differences between the periods are significant. The results are visualized through histograms comparing xG distributions during COVID and non-COVID periods, and percentage changes in xG averages across seasons are calculated and displayed using bar plots.


## Additional Performance Metrics

### `gatherPerformanceData.ipynb`
Uses the library SoccerData to scrape data from ESPN to obtain information about each match for a specified league and season.

### `analysePerformanceData.py`
Program to analyse all metrics gathered from gatherPerformanceData.ipynb. It will first take in a directory of csv files containing match data across a season for a specified league. It will append all csv files into one dataframe, and performance a statistical analysis and plot diagrams for each metric in the dataframe. The statistical tests used will be either a T-Test, or Mann-Whitney U-Test based on if the data passes the conditions for a regular T-Test. All results will be visualized in corresponding hstograms, satterplots, bxplots, and stacked bar plots.

## Running the analysis function
```bash
python3 performance/analysePerformance.py performance/performanceData
```
Inside `analysePerformance.py`, the function calls for generating the plots are currently commented out since the plots exist in the corresponding plots folder already. 
