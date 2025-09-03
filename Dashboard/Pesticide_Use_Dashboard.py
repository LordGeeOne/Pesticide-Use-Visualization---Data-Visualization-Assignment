import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# --- Page Config ---
st.set_page_config(page_title="Pesticide Use in Southern Africa", layout="wide")
st.title("🌍 Pesticide Use in Southern Africa (1990–2023)")

# --- Load CSV Data ---
data = pd.read_csv("Pesticide_Cleaned_Data_v3.csv")

country_colors = {
    "South Africa": "#1f77b4",
    "Zimbabwe": "#ff7f0e",
    "Zambia": "#2ca02c",
    "Mozambique": "#d62728",
    "Namibia": "#9467bd",
    "Botswana": "#8c564b",
    "Lesotho": "#e377c2",
    "Eswatini": "#7f7f7f",
    "Angola": "#bcbd22",
    "Malawi": "#17becf",
}

# --- Sidebar Filters ---
st.sidebar.header("Filters")
selected_countries = st.sidebar.multiselect(
    "Select countries to display",
    options=sorted(data["Country"].unique()),
    default=list(data["Country"].unique()),
)
year_range = st.sidebar.slider(
    "Select Year Range",
    int(data["Year"].min()),
    int(data["Year"].max()),
    (1990, 2023),
    step=1,
)
selected_types = st.sidebar.multiselect(
    "Select Pesticide Types",
    options=data["Pesticide_Type"].unique(),
    default=list(data["Pesticide_Type"].unique()),
)

# Filter data based on selections
filtered_data = data[
    (data["Country"].isin(selected_countries)) &
    (data["Year"] >= year_range[0]) &
    (data["Year"] <= year_range[1]) &
    (data["Pesticide_Type"].isin(selected_types))
]

# --- Sidebar Section Navigation ---
section = st.sidebar.selectbox(
    "Select Section",
    [
        "Regional Trends",
        "Overview: Average vs Latest Year",
        "Average Pesticide Use by Decade",
        "South Africa Regional Leadership",
        "Country Comparison",
        "Pesticides Breakdown",
        "Tonnes vs Kg/ha with Outliers",
    ]
)

# -----------------------
# Section: Regional Trends
# -----------------------
if section == "Regional Trends":
    st.subheader("📈 Regional Trends")
    regional = filtered_data.groupby("Year")["Kg_per_ha"].mean().reset_index()
    fig = px.line(
        regional, x="Year", y="Kg_per_ha",
        title="Average Pesticide Intensity (kg/ha)",
        height=500
    )
    fig.update_layout(title_font_size=20, xaxis_title_font_size=14, yaxis_title_font_size=14)
    st.plotly_chart(fig, use_container_width=True)
    st.write("**Insight:** Shows the average pesticide intensity across selected countries over time.")

# -----------------------
# Section: Country Comparison
# -----------------------
elif section == "Country Comparison":
    st.subheader("📊 Pesticide Use by Country")
    fig = px.line(
        filtered_data,
        x="Year",
        y="Kg_per_ha",
        color="Country",
        title="Pesticide Use Trends",
        labels={"Kg_per_ha": "Pesticide Use (kg/ha)", "Year": "Year"},
        color_discrete_map=country_colors,
        height=500
    )
    fig.update_layout(
        hovermode="x unified",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        title_font_size=20, xaxis_title_font_size=14, yaxis_title_font_size=14, legend_title_font_size=12
    )
    fig.update_traces(line=dict(width=2))
    st.plotly_chart(fig, use_container_width=True)
    st.write("**Insight:** Compare pesticide trends among selected countries.")

