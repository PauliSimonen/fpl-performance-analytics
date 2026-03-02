import requests
import pandas as pd
from datetime import datetime


# Fetch data from FPL API

URL = "https://fantasy.premierleague.com/api/bootstrap-static/"
data = requests.get(URL).json()

# List of player dictionaries

players = data["elements"]  

# Split players by position
# element_type: 1=GK, 2=DEF, 3=MID, 4=FWD

goalkeepers = [p for p in players if p["element_type"] == 1]
defenders   = [p for p in players if p["element_type"] == 2]
midfielders = [p for p in players if p["element_type"] == 3]
forwards    = [p for p in players if p["element_type"] == 4]

# Timestamp for export 
export_date = datetime.now().strftime("%d-%m-%Y")


# Define which columns to export for each position
goalkeepers_header = [
    "first_name", "second_name", "team", "minutes", "clean_sheets", "bps",
    "expected_goals_conceded_per_90", "saves_per_90", "saves", "clean_sheets_per_90"
]

defenders_header = [
    "first_name", "second_name", "team", "minutes", "clean_sheets", "bps",
    "clean_sheets_per_90", "expected_goals_conceded_per_90",
    "expected_goals_per_90", "expected_assists_per_90", "expected_goal_involvements_per_90"
]

midfielders_header = [
    "first_name", "second_name", "team", "minutes", "bps",
    "expected_assists_per_90", "expected_goals_per_90", "expected_goal_involvements_per_90", "threat"
]

forwards_header = [
    "first_name", "second_name", "team", "minutes", "bps",
    "expected_goals_per_90", "expected_goal_involvements_per_90", "threat"
]


# create a CSV from a player list and selected columns
# Adds a 'date' column for traceability
# Saves as UTF-8 with BOM so Excel shows special characters correctly

def export_position_csv(player_list, columns, filename):
    df = pd.DataFrame(player_list)
    df = df[columns]
    df["date"] = export_date
    df.to_csv(filename, index=False, encoding="utf-8-sig")


# Export CSV files

export_position_csv(goalkeepers, goalkeepers_header, "goalkeepers.csv")
export_position_csv(defenders, defenders_header, "defenders.csv")
export_position_csv(midfielders, midfielders_header, "midfielders.csv")
export_position_csv(forwards, forwards_header, "forwards.csv")