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

# -----------------------
# Section: South Africa Regional Leadership
# -----------------------
elif section == "South Africa Regional Leadership":
    st.subheader("🇿🇦 South Africa: Regional Leadership Analysis")
    sa_data = filtered_data[filtered_data["Country"]=="South Africa"].copy()
    regional_avg = filtered_data.groupby("Year")["Kg_per_ha"].mean().reset_index()
    regional_avg["Country"]="Regional Average"
    comparison_data = pd.concat([sa_data, regional_avg], ignore_index=True)

    fig, axes = plt.subplots(2,2,figsize=(16,10))

    # 1. SA vs Regional Average
    ax1 = axes[0,0]
    for country in comparison_data["Country"].unique():
        d = comparison_data[comparison_data["Country"]==country]
        style = "-" if country=="South Africa" else "--"
        width = 2.5 if country=="South Africa" else 1.5
        ax1.plot(d["Year"], d["Kg_per_ha"], label=country, linestyle=style, linewidth=width)
    ax1.set_xlabel("Year", fontsize=14)
    ax1.set_ylabel("Kg per Ha", fontsize=14)
    ax1.set_title("South Africa vs Regional Average", fontsize=16, fontweight="bold")
    ax1.tick_params(axis='x', labelsize=12)
    ax1.tick_params(axis='y', labelsize=12)
    ax1.legend(fontsize=10)
    ax1.grid(alpha=0.3)

    # 2. YoY Change
    ax2 = axes[0,1]
    sa_data_sorted = sa_data.sort_values("Year")
    sa_data_sorted["YoY_Change"] = sa_data_sorted["Kg_per_ha"].pct_change()*100
    colors = ["green" if x>0 else "red" for x in sa_data_sorted["YoY_Change"].iloc[1:]]
    ax2.bar(sa_data_sorted["Year"].iloc[1:], sa_data_sorted["YoY_Change"].iloc[1:], color=colors)
    ax2.set_xlabel("Year", fontsize=14)
    ax2.set_ylabel("Year-over-Year Change (%)", fontsize=14)
    ax2.set_title("SA: Annual Growth Rate", fontsize=16, fontweight="bold")
    ax2.axhline(0, color="black", linewidth=0.5)
    ax2.tick_params(axis='x', labelsize=12)
    ax2.tick_params(axis='y', labelsize=12)
    ax2.grid(axis="y", alpha=0.3)

    # 3. SA pesticide types evolution
    ax3 = axes[1,0]
    sa_types = sa_data[sa_data["Pesticide_Type"]!="Pesticides (total)"]
    for ptype in sa_types["Pesticide_Type"].unique():
        type_data = sa_types[sa_types["Pesticide_Type"]==ptype]
        ax3.plot(type_data["Year"], type_data["Tonnes"], label=ptype, marker="o", markersize=3)
    ax3.set_xlabel("Year", fontsize=14)
    ax3.set_ylabel("Tonnes", fontsize=14)
    ax3.set_title("SA: Pesticide Types Evolution", fontsize=16, fontweight="bold")
    ax3.tick_params(axis='x', labelsize=12)
    ax3.tick_params(axis='y', labelsize=12)
    ax3.legend(fontsize=10)
    ax3.grid(alpha=0.3)

    # 4. Comparison with neighboring countries
    ax4 = axes[1,1]
    recent_years = filtered_data[filtered_data["Year"] >= (year_range[1]-4)]
    recent_avg = recent_years.groupby("Country")["Kg_per_ha"].mean().sort_values()
    colors_bar = ["#FF6B6B" if c=="South Africa" else "#4ECDC4" for c in recent_avg.index]
    ax4.barh(recent_avg.index, recent_avg.values, color=colors_bar)
    ax4.set_xlabel("Average Kg per Ha", fontsize=14)
    ax4.set_title("Recent Performance (Last 5 Years)", fontsize=16, fontweight="bold")
    ax4.tick_params(axis='x', labelsize=12)
    ax4.tick_params(axis='y', labelsize=12)
    ax4.grid(axis="x", alpha=0.3)
    for i,(country,value) in enumerate(recent_avg.items()):
        ax4.text(value+0.05, i, f"{value:.2f}", va="center", fontsize=12)

    plt.tight_layout()
    st.pyplot(fig)
    # --- Key Insights ---
    st.markdown("""
    ###  Key Insights
    South Africa leads the region in pesticide usage per hectare, consistently above the regional average since the late 1990s.

    -  Pesticide use **tripled** from 1990 to 2023, reaching ~**3.4 kg/ha**.
    -  **Herbicides dominate** pesticide use, followed by fungicides; insecticides are least used.
    -  Growth has been **volatile but resilient**, bouncing back quickly after downturns.
    -  In the last 5 years, **Eswatini and Botswana surpassed South Africa** in intensity, but SA remains a **top user regionally**.
    """)

# -----------------------
# Section: Pesticides Breakdown
# -----------------------
elif section == "Pesticides Breakdown":
    st.subheader("🧪 Pesticides Breakdown by Type")

    pesticide_types = filtered_data[filtered_data["Pesticide_Type"] != "Pesticides (total)"].copy()
    if pesticide_types.empty:
        st.warning("No data available for the selected filters.")
    else:
        type_summary = pesticide_types.groupby(['Country', 'Pesticide_Type'])['Tonnes'].mean().reset_index()
        type_pivot = type_summary.pivot(index='Country', columns='Pesticide_Type', values='Tonnes').fillna(0)

        # --- Stacked Bars ---
        fig6, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 6), constrained_layout=True)

        type_pivot.plot(kind='bar', stacked=True, ax=ax1, color=plt.cm.Set2.colors[:type_pivot.shape[1]])
        ax1.set_xlabel('Country', fontsize=14)
        ax1.set_ylabel('Average Pesticide Use (tonnes)', fontsize=14)
        ax1.set_title('Average Pesticide Use by Type (1990–2023)', fontsize=16, fontweight='bold')
        ax1.tick_params(axis='x', labelsize=12)
        ax1.tick_params(axis='y', labelsize=12)
        ax1.legend(title='Pesticide Type', bbox_to_anchor=(1.05,1), loc='best', fontsize=14)
        ax1.grid(axis='y', alpha=0.3)
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=12)

        type_pivot_pct = type_pivot.div(type_pivot.sum(axis=1), axis=0) * 100
        type_pivot_pct.plot(kind='bar', stacked=True, ax=ax2, color=plt.cm.Set2.colors[:type_pivot.shape[1]])
        ax2.set_xlabel('Country', fontsize=14)
        ax2.set_ylabel('Percentage (%)', fontsize=14)
        ax2.set_title('Pesticide Type Composition by Country', fontsize=16, fontweight='bold')
        ax2.tick_params(axis='x', labelsize=12)
        ax2.tick_params(axis='y', labelsize=12)
        ax2.legend(title='Pesticide Type', bbox_to_anchor=(1.05,1), loc='upper left', fontsize=10)
        ax2.grid(axis='y', alpha=0.3)
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=14)

        st.pyplot(fig6)
        st.write("**Insight:** Left chart shows absolute use per type; right chart shows composition per country.")

        # --- Pie Charts ---
        fig7, axes = plt.subplots(1, 2, figsize=(14,6))

        # South Africa Pie
        sa_data = type_pivot.loc['South Africa'] if 'South Africa' in type_pivot.index else pd.Series()
        if not sa_data.empty:
            axes[0].pie(sa_data, labels=sa_data.index, autopct='%1.1f%%', startangle=90, textprops={'fontsize':12})
            axes[0].set_title("South Africa Pesticide Composition", fontsize=14, fontweight='bold')
        else:
            axes[0].text(0.5,0.5,"No data for South Africa", ha='center', va='center', fontsize=12)

        # Global Pie
        global_data = type_pivot.mean(axis=0)
        axes[1].pie(global_data, labels=global_data.index, autopct='%1.1f%%', startangle=90, textprops={'fontsize':12})
        axes[1].set_title("Global Pesticide Composition (Selected Countries)", fontsize=14, fontweight='bold')

        st.pyplot(fig7)
        # --- Key Insights for Pesticide Breakdown ---
        st.markdown("""
        ###  Key Insights
        -  **Herbicides dominate** pesticide use both in **South Africa (40%)** and **globally (~39%)**.
        -  **Fungicides** are the second largest category, making up **~34–35%** of use.
        -  **Insecticides** have the smallest share, especially in South Africa (**25% vs global 28%**).
        -  South Africa’s pesticide mix **aligns closely with global trends**, but with slightly **heavier herbicide dependence**.
        """)

