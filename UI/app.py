import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import datetime
import time 
import sys
import os
import random
import pkg_resources
from PIL import Image
from lime.lime_tabular import LimeTabularExplainer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../data_handler")))
from data_loader import DataLoader
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../machine_learning")))
from rating_predictions import PlayerPrediction 
st.set_page_config(page_title="Forza Football AI", page_icon=":soccer:", layout="wide")

# zip_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
# data_loader = DataLoader(zip_folder=zip_folder_path)

# dataframes = data_loader.process_data()

# for filename, df in dataframes.items():
#     print(f"Förhandsvisning av {filename}:")
#     st.write(df.head(), "\n")

def explain_with_lime(model, X_train, X_test, instance_index):
    explainer = LimeTabularExplainer(
        X_train.values,
        feature_names=X_train.columns.tolist(),
        mode="regression",
        verbose=True
    )
    exp = explainer.explain_instance(
        X_test.iloc[instance_index].values,
        model.predict,
        num_features=10
    )
    return exp

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
    # Skapa scatterplot
    fig = px.scatter(
        x=y_test,
        y=y_pred,
        labels={'x': 'Actual Rating', 'y': 'Predicted Rating'},
        title="Actual vs Predicted Ratings",
        width=700,
        height=500
    )
    
    # Lägg till perfekt prediktionslinje
    fig.add_trace(
        go.Scatter(
            x=[1, 10],
            y=[1, 10],
            mode='lines',
            name='Perfect Prediction',  # Legend-namn här
            line=dict(color='red', dash='dash')
        )
    )
    
    # Uppdatera layout för tydlig legend
    fig.update_layout(
        legend=dict(
            orientation="h",  # Horisontell legend
            yanchor="bottom",
            y=1.02,          # Placera ovanför plotten
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
# def plot_graph(y_test, y_pred):
#     plt.figure(figsize=(10, 6))

#     plt.scatter(y_test, y_pred, color="blue", alpha=0.5, label="Predicted values")
#     plt.plot([y_test.min(), y_test.max()], [y_pred.min(), y_pred.max()], color="red", linestyle="-", label="The perfect prediction line")

#     plt.legend()

#     plt.xlim(1, 10)
#     plt.ylim(1, 10)

#     plt.title("Comparison of Actual vs Predicted Player Ratings")
#     plt.xlabel("Actual Player Rating")
#     plt.ylabel("Predicted Player Rating")

#     st.pyplot(plt, clear_figure=True)

@st.cache_data
def load_and_filter_data():
    df = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Players.csv")))
    return df


def main():
    df = load_and_filter_data()
    y_train, y_pred, mse, mae, r2 = load_predictions()
   
    with st.sidebar:
        st.title("⚙️ Kontrollpanel")  # Titel med emoji
        
        # Välj sida (om du har flera sidor)
        selected_page = st.radio(
            "Meny",
            ["Hem", "Roadmap", "Data", "Modell", "Pipeline", "Inställningar"],
            index=0
        )
        
        # Globala inställningar (exempel)
        st.divider()
        st.write("**Inställningar**")
        dark_mode = st.toggle("Mörkt läge 🌙")
        debug_mode = st.toggle("Debug-läge", help="Aktivera för tekniska detaljer")
        
        # Snabblänkar
        st.divider()
    
    if selected_page == "Hem":
        col1, col2, col3, col4 = st.columns([0.25, 0.25, 0.25, 0.25])
        with col1:
            # Ladda upp Forzas logga (ersätt med din bildfil)
            logo = Image.open("../forza.png")
            st.image(logo, width=200)
        with col2:
            st.title("Forza AI Hub")
            st.markdown("""
            *🤖 Utvecklad med Machine Learning*
                        
            *🌳 Tränad med random forest regression*
                        
            *⚽ Skulle kunna vidareutvecklas med Forza API data*
    """)
        
          
    if selected_page == "Roadmap":
    # Initiera status om den inte finns
        if 'roadmap_status' not in st.session_state:
            st.session_state.roadmap_status = ["⚪ Planerad"] * 4

        with st.expander("🚀 12-veckors Roadmap (Klicka för att se planen)"):
            # Visa roadmap-tabellen (samma som tidigare)
            st.markdown(f"""
            | Vecka | Fokus                     | Leverabler                             | Status       |
            |-------|---------------------------|----------------------------------------|--------------|
            | 1-2   | **Data Pipeline**         | Automatiserad datainsamling från datakällor | {st.session_state.roadmap_status[0]} |
            | 3-5   | **Modelloptimering**      | Optimera modellen, SHAP-förklaringar                | {st.session_state.roadmap_status[1]} |
            | 6-8   | **API-Integration**       | FastAPI-endpoint för betyg                  | {st.session_state.roadmap_status[2]} |
            | 9-12  | **Användartester**        | Integrera API från OpenAI som förklara betyget för a               | {st.session_state.roadmap_status[3]} |
            """)

            ### --- LÄGG KNAPPARNA HÄR UNDER TABELLEN --- ###
            cols = st.columns([1, 1, 1, 1])
            with cols[0]:
                if st.button("Sprint 1-2 klar", help="Markera som avslutad"):
                    st.session_state.roadmap_status[0] = "✅ Klar"
                    st.rerun()
            with cols[1]:
                if st.button("Sprint 3-5 klar", help="Markera som avslutad"):
                    st.session_state.roadmap_status[1] = "✅ Klar"
                    st.rerun()
            with cols[2]:
                if st.button("Sprint 6-8 klar", help="Markera som avslutad"):
                    st.session_state.roadmap_status[2] = "✅ Klar"
                    st.rerun()
            with cols[3]:
                if st.button("Sprint 9-12 klar", help="Markera som avslutad"):
                    st.session_state.roadmap_status[3] = "✅ Klar"
                    st.rerun()
            ### ------------------------------------------ ###

            # Progressbar som uppdateras automatiskt
            completed = st.session_state.roadmap_status.count("✅ Klar")
            st.progress(completed / 4, text=f"{completed}/4 sprintar klara")

            # Global uppdateringsknapp (alternativ)
            if st.button("Återställ alla statusar"):
                st.session_state.roadmap_status = ["⚪ Planerad"] * 4
                st.rerun()

    if selected_page == "Modell":
        
        with st.expander("🤖 Hur presterar Forza Football AI?"):
            y_test, y_pred, mse, mae, r2 = load_predictions()
            st.write(f"Mean Squared Error: {mse:.2f}")
            st.write(f"Mean Absolute Error: {mae:.2f}")
            st.write(f"R²: {r2:.2f}")
            with st.container():
                plot_graph(y_test, y_pred)


        with st.expander("🌳 Hur funkar Random Forest?"):

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

    

        with st.expander("📊 Vill du betygsätta Messi säsongen 2018-2019?"):
            user_rating = st.slider("Välj en rating mellan 1-10", min_value=1, max_value=10, value=5)

            rating_placeholder = st.empty()

            # Initiera session_state om det inte finns
            if "betyg_genererat" not in st.session_state:
                st.session_state.betyg_genererat = False

            if st.button("Generera betyg"):
                with st.spinner("AI tänker... 🤖"):
                    ai_rating = random.randint(10, 10)  # Messi är alltid 10 😆
                    time.sleep(2)
                    st.session_state.betyg_genererat = True  # Markera att betyg har genererats
                    
                    # Uppdatera texten efter knappen
                    rating_placeholder.write(f"👨 Ditt betyg: {user_rating}. \n\n🤖 AI betyg: {ai_rating}.")

            # Visa knappen för att fråga varför bara efter att betyget är genererat
            if st.session_state.betyg_genererat:
                if st.button("🤖 Varför ger jag detta betyg till Messi säsongen 2018-2019?"):
                    with st.spinner("AI skriver... 🤖"):
                        time.sleep(2)
                        st.write("Jag ger Messi betyget 10 eftersom han gjorde 51 mål på 50 matcher och vann Ballon d'Or.")

    if selected_page == "Data":
        file_path = "../extracted_data/Cleaned_Standard_stats.csv"
        df_raw = pd.read_csv(file_path)

        with st.expander("✍️ Cleanad tabell (kraftigt minimerad)"):
            st.dataframe(df[["Team", "Player", "Season", "Pos", "PositionWeightedRating"]])
        with st.expander("✍️ En av original dataseten"):
            st.dataframe(df_raw)

    if selected_page == "Pipeline":
        col1, col2 = st.columns([1, 1])
        with col1:
            with st.expander("🚀 Hela ML-pipelinen (från data till prediktion)"):
                st.markdown("""
                ### **1️⃣ Data Extraction**  
                - Automatiserad hämtning från Forza API (simulerad i PoC)  
                - Exempel: `Cleaned_Standard_stats.csv`  

                ### **2️⃣ Data Cleaning**  
                - Hantering av saknade värden  
                - Position-specifika features (t.ex. `Tackle%` för försvarare)  

                ### **3️⃣ Feature Engineering**  
                - Z-scoring per position  
                - Liga-justeringar (t.ex. Premier League ×1.0)  

                ### **4️⃣ Modellträning**  
                - Random Forest med 350 träd  
                - MAE: **0.44** på testdata  

                ### **5️⃣ Deployment**  
                - Webbapp med Streamlit  
                - Redo för API-integration  
                """)
            with col2:
                st.graphviz_chart("""
                digraph {
                    node [shape=box];
                    graph [dpi=70, size="10,8"];
                    "Raw Data" -> "Data Cleaning";
                    "Data Cleaning" -> "Feature Engineering";
                    "Feature Engineering" -> "Model Training";
                    "Model Training" -> "Web App";
                    "Web App" -> "Forza API (nästa steg)";
                }
                """)


                    
     


if __name__ == "__main__":
    main()