import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import time
import pandas as pd
import sys
import os
import random
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

@st.cache_data
def load_predictions():
    players_csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Players.csv"))
    prediction = PlayerPrediction(players_csv_path)
    X_train, X_test, y_train, y_test = prediction.prepare_data()
    model = prediction.train_model(X_train, y_train)
    y_pred, mse, mae, r2 = prediction.evaluate_model(model, X_test, y_test)
    return y_test, y_pred, mse, mae, r2

@st.cache_data
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

@st.cache_data
def load_and_filter_data():
    df = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Players.csv")))
    return df

def main():
    df = load_and_filter_data()
    st.set_page_config(page_title="Forza Football AI", page_icon=":soccer:")
    
    with st.expander("🤖 Hur presterar Forza Football AI?"):
        y_test, y_pred, mse, mae, r2 = load_predictions()
        st.write(f"Mean Squared Error: {mse:.2f}")
        st.write(f"Mean Absolute Error: {mae:.2f}")
        st.write(f"R²: {r2:.2f}")
        plot_graph(y_test, y_pred)


    with st.expander("Hur funkar Random Forest?"):

        # Samla data knapp med tooltip
        if st.button('1. Samla data', help="Här samlar vi data som ska användas för att träna modellen. Det kan vara data från olika källor som CSV-filer, databaser eller API:er."):
            pass  # Här kan du lägga till ytterligare funktionalitet om du vill

        # Rensa data knapp med tooltip
        if st.button('2. Rensa data', help="I detta steg rensar vi datan genom att ta bort saknade värden, hantera uteliggare och kategorisera variabler om det behövs."):
            pass
        
        # Bygg och träna modellen knapp med tooltip
        if st.button('3. Bygg och träna modellen', help="Vi bygger vår Random Forest-modell genom att träna flera beslutsträd på våra data. Varje träd lär sig olika delar av datan för att ge bättre generalisering."):
            pass
        
        # Utvärdera modellen knapp med tooltip
        if st.button('4. Utvärdera modellen', help="Efter att ha tränat modellen utvärderar vi dess prestanda genom att använda testdata och beräkna t.ex. MSE, MAE och MSE."):
            pass
        
        # Använd modellen för prediktion knapp med tooltip
        if st.button('5. Använd modellen för prediktion', help="När modellen är tränad och utvärderad, kan den användas för att göra prediktioner på nya data."):
            pass


    with st.expander("Original-tabell skapad av mig"):
        df = df[df["Player"] == "dusantadic"]
        st.dataframe(df[["Team", "Player", "Season", "Pos", "PositionWeightedRating"]])

    with st.expander("Vill du betygsätta Messi säsongen 2018-2019?"):
        user_rating = st.selectbox("Välj en rating mellan 1-10", list(range(1, 11)))

        rating_placeholder = st.empty()

        if user_rating:
            with st.spinner("AI tänker... 🤖"):
                ai_rating = random.randint(8, 10)
                time.sleep(2)
                rating_placeholder.write(f"Ditt betyg: {user_rating}.")
                rating_placeholder.write(f"🤖 AI betyg: {ai_rating}.")
                
                


if __name__ == "__main__":
    main()