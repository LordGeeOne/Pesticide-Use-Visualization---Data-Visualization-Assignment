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

# -----------------------
# Section: Overview: Average vs Latest Year
# -----------------------
elif section == "Overview: Average vs Latest Year":
    st.subheader("🌍 Overview: Average vs Latest Year")
    fig3, (ax1, ax2) = plt.subplots(1, 2, figsize=(21, 8))

    avg_per_country = filtered_data.groupby("Country")["Kg_per_ha"].mean().sort_values()
    ax1.barh(
        avg_per_country.index,
        avg_per_country.values,
        color=[country_colors.get(c, "#666666") for c in avg_per_country.index]
    )
    ax1.set_xlabel("Average Pesticide Use (kg/ha)", fontsize=14)
    ax1.set_ylabel("Country", fontsize=14)
    ax1.set_title("Average Pesticide Use Intensity by Country", fontsize=16, fontweight="bold")
    ax1.tick_params(axis='x', labelsize=12)
    ax1.tick_params(axis='y', labelsize=12)
    ax1.grid(axis="x", alpha=0.3)
    for i, (country_name, value) in enumerate(avg_per_country.items()):
        ax1.text(value + 0.05, i, f"{value:.2f}", va="center", fontsize=12)

    latest_year_data = filtered_data[filtered_data["Year"] == year_range[1]]
    latest_per_country = latest_year_data.groupby("Country")["Kg_per_ha"].mean().sort_values()
    ax2.barh(
        latest_per_country.index,
        latest_per_country.values,
        color=[country_colors.get(c, "#666666") for c in latest_per_country.index]
    )
    ax2.set_xlabel("Pesticide Use (kg/ha)", fontsize=14)
    ax2.set_ylabel("Country", fontsize=14)
    ax2.set_title(f"Pesticide Use Intensity in {year_range[1]}", fontsize=16, fontweight="bold")
    ax2.tick_params(axis='x', labelsize=12)
    ax2.tick_params(axis='y', labelsize=12)
    ax2.grid(axis="x", alpha=0.3)
    for i, (country_name, value) in enumerate(latest_per_country.items()):
        ax2.text(value + 0.05, i, f"{value:.2f}", va="center", fontsize=12)

    plt.tight_layout()
    st.pyplot(fig3)
    st.write("**Insight:** Average and latest year pesticide use per country.")

# -----------------------
# Section: Average Pesticide Use by Decade
# -----------------------
elif section == "Average Pesticide Use by Decade":
    st.subheader("📊 Average Pesticide Use per Hectare by Decade")
    conn = sqlite3.connect("Pesticide_Uses_ZA.db")
    df_db = pd.read_sql_query("SELECT * FROM Pesticide_Uses;", conn)
    conn.close()
    df_db = df_db[df_db["Pesticide_Type"].isin(selected_types)]
    df_db = df_db[df_db["Country"].isin(selected_countries)]
    df_db = df_db[(df_db["Year"] >= year_range[0]) & (df_db["Year"] <= year_range[1])]

    def get_decade(year):
        if 1990 <= year <= 1999: return "1990s"
        elif 2000 <= year <= 2009: return "2000s"
        elif 2010 <= year <= 2019: return "2010s"
        elif 2020 <= year <= 2023: return "2020s"
        else: return "Other"

    df_db["Decade"] = df_db["Year"].apply(get_decade)
    avg_decade = df_db.groupby("Decade", as_index=False)["Kg_per_ha"].mean().rename(columns={"Kg_per_ha":"Avg_Kg_per_ha"})
    st.dataframe(avg_decade)

    first_decade = avg_decade["Avg_Kg_per_ha"].iloc[0]
    last_decade = avg_decade["Avg_Kg_per_ha"].iloc[-1]
    pct_increase = ((last_decade - first_decade) / first_decade) * 100
    st.write(f"Average use per hectare increased by **{pct_increase:.2f}%** from {avg_decade['Decade'].iloc[0]} to {avg_decade['Decade'].iloc[-1]}.")

    fig4, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x="Decade", y="Avg_Kg_per_ha", data=avg_decade, palette="Set2", ax=ax)
    for index, row in avg_decade.iterrows():
        ax.text(index, row.Avg_Kg_per_ha/2, f"{row.Avg_Kg_per_ha:.2f}", ha="center", va="center", color="white", fontweight="bold", fontsize=12)
    ax.set_title("Average Pesticide Use per Hectare by Decade", fontsize=16, fontweight="bold")
    ax.set_ylabel("Avg Kg per Ha", fontsize=14)
    ax.set_xlabel("Decade", fontsize=14)
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    st.pyplot(fig4)
    st.write("**Insight:** Shows how pesticide use per hectare changed across decades.")

