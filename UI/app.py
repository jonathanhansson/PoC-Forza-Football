import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../data_handler")))
from data_loader import DataLoader

zip_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
data_loader = DataLoader(zip_folder=zip_folder_path)

dataframes = data_loader.process_data()

for filename, df in dataframes.items():
    print(f"Förhandsvisning av {filename}:")
    st.write(df.head(), "\n")