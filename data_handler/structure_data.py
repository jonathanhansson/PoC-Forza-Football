import pandas as pd
import streamlit as st
from fetch_data import get_api_data

def structure_data():
    data = get_api_data() # Hämtar datan från fetch_data-filen
    df = pd.DataFrame(data) # Gör om listan till en dataframe

    return df
