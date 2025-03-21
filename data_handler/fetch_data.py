import requests
import pandas as pd
import streamlit as st

# -----------------------------------------------------------------------

api_key = "e547ef531e5848919c3dfe43d910d435"
base_url_competition = "https://api.football-data.org/v4/competitions"
base_url_player = "https://api.football-data.org/v4/persons"
    
# -----------------------------------------------------------------------

def fetch_games(competition, season=2023):
    url = f"{base_url_competition}/{competition}/matches?season={season}"

    headers = {
        "X-Auth-Token": api_key
    }

    # Hämtar data från API
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {}
    
# -----------------------------------------------------------------------    

def fetch_all_players():
    url = f"{base_url_player}/players"  # Här kan du ändra beroende på API
    headers = {"X-Auth-Token": api_key}
    
    # Hämtar data från API
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {}

# -----------------------------------------------------------------------  

def fetch_player(id):
    url = f"{base_url_player}/{id}"

    headers = {
        "X-Auth-Token": api_key
    }

    # Hämtar data från API
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {}

# -----------------------------------------------------------------------

def fetch_player_goals(id):
    url = f"{base_url_player}/{id}/matches?e=GOAL&limit=5"

    headers = {
        "X-Auth-Token": api_key
    }

    # Hämtar data från API
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {}
# -----------------------------------------------------------------------