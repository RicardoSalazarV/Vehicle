import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import requests
from io import StringIO

# Configuración inicial de Streamlit
st.set_page_config(
    page_title="Análisis de Vehículos",
    page_icon="🚗",
    layout="wide"
)

# Función para cargar el dataset desde GitHub
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/RicardoSalazarV/Vehicle/refs/heads/main/Data/vehicles.csv"
    response = requests.get(url)

    if response.status_code == 200:
        # Cargar el CSV en pandas
        df = pd.read_csv(StringIO(response.text))

        # Preprocesamiento
        df['date_posted'] = pd.to_
