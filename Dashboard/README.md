# 🌍 Pesticide Use Dashboard

## 🚀 Live Dashboard

**🔗 [View Live Dashboard](https://pesticide-use-visualization.streamlit.app/)**

> Interactive web application deployed on Streamlit Cloud - access the dashboard instantly!

## 📊 Dashboard Overview

This interactive Streamlit dashboard visualizes pesticide use trends in Southern Africa from 1990-2023. Explore comprehensive data analysis with multiple visualization sections and interactive filtering options.

## 🏃‍♂️ Quick Start

### Option 1: Use Live Dashboard (Recommended)
Simply click the link above to access the deployed dashboard - no setup required!

### Option 2: Run Locally

1. **Navigate to this directory**
   ```bash
   cd Dashboard
   ```

2. **Install dependencies** (if not already installed)
   ```bash
   pip install streamlit pandas plotly matplotlib seaborn
   ```

3. **Run the dashboard**
   ```bash
   streamlit run Pesticide_Use_Dashboard.py
   ```

4. **Open your browser** to `http://localhost:8501`

## 📁 Files in This Directory

- `Pesticide_Use_Dashboard.py` - Main dashboard application
- `Pesticide_Cleaned_Data_v3.csv` - Dataset used by the dashboard
- `Pesticide_Uses_ZA.db` - SQLite database for decade analysis
- `README.md` - This file

## 🎯 Dashboard Features

- **7 Interactive Sections**: Regional trends, country comparisons, decade analysis, and more
- **Dynamic Filtering**: Filter by countries, years, and pesticide types
- **Interactive Charts**: Plotly and Matplotlib visualizations
- **Navigation System**: Easy section-to-section navigation with buttons
- **Responsive Design**: Clean, modern interface with green theme

## 🌍 Data Coverage

- **10 Southern African Countries**
- **1990-2023 Time Period**
- **Multiple Pesticide Types**: Herbicides, Fungicides, Insecticides
- **Comprehensive Metrics**: Usage intensity (kg/ha) and trends

## 🔧 Troubleshooting

### Data File Issues
The dashboard automatically handles different deployment environments and will look for data files in multiple locations.

### Performance
- Use filters to focus on specific countries or time periods
- The dashboard is optimized for interactive exploration

## 📝 Notes

This dashboard is part of a larger data visualization project. For the complete analysis including the Jupyter notebook, see the parent directory.
