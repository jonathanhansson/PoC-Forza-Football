import requests
import pandas as pd
import streamlit as st

def get_api_data():
    # API-nyckel och URL
    api_key = "e547ef531e5848919c3dfe43d910d435"
    url = "https://api.football-data.org/v4/competitions/PL/matches?season=2023"

    # Headers för API-anrop
    headers = {
        "X-Auth-Token": api_key
    }

    # Hämta data från API
    response = requests.get(url, headers=headers)

    # Kontrollera om svaret är framgångsrikt
    if response.status_code == 200:
        match_data = response.json()
        
        # Lista för att spara all matchinformation
        matches_info = []

        # Iterera över alla matcher i JSON-datan
        for match in match_data['matches']:
            match_info = {
                'match_id': match['id'],
                'competition_id': match['competition']['id'],
                'competition_name': match['competition']['name'],
                'season_id': match['season']['id'],
                'season_start': match['season']['startDate'],
                'season_end': match['season']['endDate'],
                'match_date': match['utcDate'],
                'status': match['status'],
                'matchday': match['matchday'],
                'stage': match['stage'],
                'home_team_id': match['homeTeam']['id'],
                'home_team_name': match['homeTeam']['name'],
                'home_team_short_name': match['homeTeam']['shortName'],
                'home_team_tla': match['homeTeam']['tla'],
                'home_team_crest': match['homeTeam']['crest'],
                'away_team_id': match['awayTeam']['id'],
                'away_team_name': match['awayTeam']['name'],
                'away_team_short_name': match['awayTeam']['shortName'],
                'away_team_tla': match['awayTeam']['tla'],
                'away_team_crest': match['awayTeam']['crest'],
                'full_time_home_score': match['score']['fullTime']['home'],
                'full_time_away_score': match['score']['fullTime']['away'],
                'half_time_home_score': match['score']['halfTime']['home'],
                'half_time_away_score': match['score']['halfTime']['away'],
                'referee_id': match['referees'][0]['id'],
                'referee_name': match['referees'][0]['name'],
                'referee_type': match['referees'][0]['type'],
                'referee_nationality': match['referees'][0]['nationality']
            }

            matches_info.append(match_info)
        
        return matches_info

    else:   
        print(f"API request failed with status code: {response.status_code}")
        return None
