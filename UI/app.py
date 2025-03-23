import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../data_handler")))
from data_loader import DataLoader
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../machine_learning")))
from rating_predictions import PlayerPrediction

# zip_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
# data_loader = DataLoader(zip_folder=zip_folder_path)

# dataframes = data_loader.process_data()

# for filename, df in dataframes.items():
#     print(f"Förhandsvisning av {filename}:")
#     st.write(df.head(), "\n")
    
def load_predictions():
    players_csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Players.csv"))
    prediction = PlayerPrediction(players_csv_path)
    X_train, X_test, y_train, y_test = prediction.prepare_data()
    model = prediction.train_model(X_train, y_train)
    y_pred = prediction.evaluate_model(model, X_test, y_test)
    return y_test, y_pred

def plot_graph(y_test, y_pred):
    plt.figure(figsize=(15, 15))

    plt.scatter(y_test, y_pred, color="blue", alpha=0.5, label="Predicted values")
    
    min_val = min(y_test.min(), y_pred.min())  # Gemensamt min
    max_val = max(y_test.max(), y_pred.max())  # Gemensamt max
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', label="Perfect line")   

    plt.legend()

    plt.xlim(1, 10)
    plt.ylim(1, 10)

    plt.title("Comparison of Actual vs Predicted Player Ratings")
    plt.xlabel("Actual Player Rating")
    plt.ylabel("Predicted Player Rating")

    st.pyplot(plt)

def plot_radar(player_name, df):
    player_stats = df[df["Player"] == player_name][["Goals_90_z", "Assists_90_z", "Tackle%_z", "Interceptions_z"]]
    fig = px.line_polar(
        player_stats, 
        r=player_stats.values[0], 
        theta=player_stats.columns,
        line_close=True,
        color_discrete_sequence=["#FF6B6B"],  # Forza-färger? 😉
        title=f"Spelarprofil: {player_name}"
    )
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)")  # Genomskinlig bakgrund
    st.plotly_chart(fig)

def main():
    st.title("Player rating prediction comparison")

    players_csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Players.csv"))
    df = pd.read_csv(players_csv_path)

    y_test, y_pred = load_predictions()


    plot_graph(y_test, y_pred)
    selected_player = st.selectbox("Välj spelare: ", df["Key"].str[10:])
    plot_radar(selected_player, df)

if __name__ == "__main__":
    main()