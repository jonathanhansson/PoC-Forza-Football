import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../data_handler")))
from structure_data import structure_data

def layout():
    df = structure_data()
    st.write(df)

layout()