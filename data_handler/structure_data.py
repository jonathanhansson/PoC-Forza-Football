import pandas as pd
import streamlit as st

# -----------------------------------------------------------------------

def structure_games(game_data):
    games = game_data.get("matches", [])

    if not games:
        print("No games found for this season")

    structured_data = []

    for game in games:
        structured_data.append({
            "Match ID": game.get("id"),
            "Datum": game.get("utcDate"),
            "Hemmalag": game["homeTeam"]["name"],
            "Bortalag": game["awayTeam"]["name"],
            "Resultat": f"{game['score']['fullTime']['home']} - {game['score']['fullTime']['away']}"
        })
    return pd.DataFrame(structured_data)

# -----------------------------------------------------------------------

def structure_players(player_data):
    # Om vi får ett enda spelarobjekt, packa det i en lista
    if isinstance(player_data, dict):
        players = [player_data]
    elif isinstance(player_data, list):
        players = player_data
    else:
        players = []

    if not players:
        print("No player data found")
        return pd.DataFrame()

    structured_players = []
    for player in players:
        structured_players.append({
            "Player ID": player.get("id"),
            "Name": player.get("name"),
            "Date of Birth": player.get("dateOfBirth"),
            "Nationality": player.get("nationality"),
            "Section": player.get("section"),
            "Position": player.get("position"),
            "Shirt Number": player.get("shirtNumber"),
            "Last Updated": player.get("lastUpdated"),
            "Current Team": player.get("currentTeam", {}).get("name")
        })
    return pd.DataFrame(structured_players)

# -----------------------------------------------------------------------




    
