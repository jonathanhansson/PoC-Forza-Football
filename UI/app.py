import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../data_handler")))
from structure_data import structure_games, structure_players
from fetch_data import fetch_games, fetch_player, fetch_player_goals

# -----------------------------------------------------------------------

st.title("Football data viewer")

available_leagues = ["PL", "SA", "PD", "BL1", "FL1"]
league = st.selectbox("Välj liga: ", available_leagues)

if st.button("Hämta ligastatistik"):
    game_data = fetch_games(league, 2023)
    df = structure_games(game_data)
    st.write("Displaying info about games from 2023/2024 season")
    st.write(df)

# -----------------------------------------------------------------------

available_players = [i for i in range(1, 101)]
player = st.selectbox("Välj spelare: ", available_players)

if st.button("Hämta spelare"):
    player_data = fetch_player(player)
    df = structure_players(player_data)
    st.write(df)

# -----------------------------------------------------------------------

hey = [44]
player = st.selectbox("Välj spelare: ", hey)

if st.button("Se mål: "):
    goal_data = fetch_player_goals(player)
    st.write(goal_data)

# -----------------------------------------------------------------------