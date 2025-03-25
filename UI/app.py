import matplotlib.pyplot as plt
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
    plt.figure(figsize=(10, 6))

    plt.scatter(y_test, y_pred, color="blue", alpha=0.5, label="Predicted values")
    plt.plot([y_test.min(), y_test.max()], [y_pred.min(), y_pred.max()], color="red", linestyle="-", label="The perfect prediction line")

    plt.legend()

    plt.xlim(1, 10)
    plt.ylim(1, 10)

    plt.title("Comparison of Actual vs Predicted Player Ratings")
    plt.xlabel("Actual Player Rating")
    plt.ylabel("Predicted Player Rating")

    st.pyplot(plt)

def main():
    st.title("Player rating prediction comparison")

    y_test, y_pred = load_predictions()

    plot_graph(y_test, y_pred)

if __name__ == "__main__":
    main()