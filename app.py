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
        df['date_posted'] = pd.to_datetime(df['date_posted'])
        df['vehicle_age'] = df['date_posted'].dt.year - df['model_year']
        df['condition_simplified'] = df['condition'].map({
            'excellent': 1, 'like new': 1, 'good': 0, 'fair': 0, 'salvage': 0
        })
        df['is_4wd'].fillna(0, inplace=True)
        df['is_4wd'] = df['is_4wd'].astype(int)
        return df
    else:
        st.error(f"Error al descargar el archivo: {response.status_code}")
        return pd.DataFrame()  # Retorna un DataFrame vacío en caso de error

# Cargar los datos
df = load_data()

# Título de la app
st.title("🚗 Exploración Interactiva de Vehículos")

# Sidebar con filtros interactivos
st.sidebar.header("Filtros")
price_range = st.sidebar.slider("Rango de precio", int(df['price'].min()), int(df['price'].max()), (5000, 25000))
vehicle_age_range = st.sidebar.slider("Rango de edad del vehículo", 0, int(df['vehicle_age'].max()), (0, 10))
selected_types = st.sidebar.multiselect("Tipo de vehículo", options=df['type'].unique(), default=df['type'].unique())
selected_condition = st.sidebar.radio("Condición del vehículo", ["Todas", "Excelente/Como nuevo", "Buena/Regular"], index=0)

# Aplicar filtros
filtered_df = df[
    (df['price'] >= price_range[0]) & 
    (df['price'] <= price_range[1]) & 
    (df['vehicle_age'] >= vehicle_age_range[0]) & 
    (df['vehicle_age'] <= vehicle_age_range[1]) & 
    (df['type'].isin(selected_types))
]
if selected_condition == "Excelente/Como nuevo":
    filtered_df = filtered_df[filtered_df['condition_simplified'] == 1]
elif selected_condition == "Buena/Regular":
    filtered_df = filtered_df[filtered_df['condition_simplified'] == 0]

# Mostrar estadísticas generales
with st.expander("📊 Estadísticas generales", expanded=True):
    st.write(f"### Datos Filtrados ({len(filtered_df)} registros)")
    st.dataframe(filtered_df.describe())
    show_data = st.checkbox("Mostrar datos completos")
    if show_data:
        st.write(filtered_df)

# Visualizaciones interactivas
st.write("## Visualizaciones")

# 1. Botón para construir un histograma
if st.button("Construir histograma interactivo"):
    st.write("### Creación de un histograma para la columna `odometer`")
    fig_hist = px.histogram(
        filtered_df, 
        x="odometer", 
        title="Histograma de kilometraje (`odometer`)",
        labels={"odometer": "Kilometraje"},
        nbins=30
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# 2. Botón para construir un gráfico de dispersión
if st.button("Construir gráfico de dispersión interactivo"):
    st.write("### Gráfico de dispersión entre `price` y `odometer`")
    fig_scatter = px.scatter(
        filtered_df, 
        x="odometer", 
        y="price", 
        color="condition",
        title="Relación entre precio y kilometraje (`odometer`)",
        labels={"odometer": "Kilometraje", "price": "Precio"},
        size="vehicle_age", 
        hover_data=["model", "type"]
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# 3. Visualizaciones adicionales con checkboxes
if st.checkbox("Mostrar distribución de colores de pintura"):
    st.write("### Distribución de Colores de Pintura")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=filtered_df, y='paint_color', order=filtered_df['paint_color'].value_counts().index, palette='muted', ax=ax)
    ax.set_title("Distribución de Colores de Pintura")
    ax.set_xlabel("Frecuencia")
    ax.set_ylabel("Color de Pintura")
    st.pyplot(fig)

if st.checkbox("Mostrar precio por tipo de vehículo"):
    st.write("### Precio por Tipo de Vehículo")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=filtered_df, x='type', y='price', palette='coolwarm', ax=ax)
    ax.set_title("Precio por Tipo de Vehículo")
    ax.set_xlabel("Tipo de Vehículo")
    ax.set_ylabel("Precio")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)