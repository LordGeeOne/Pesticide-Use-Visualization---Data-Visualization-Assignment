# 🌍 Pesticide Use in Southern Africa Dashboard

An interactive dashboard visualizing pesticide use trends in Southern Africa (1990–2023). Explore country comparisons, decade averages, pesticide type breakdowns, and outlier detection using Streamlit, Plotly, and Matplotlib.

## 📊 Features

- **Regional Trends**: Average pesticide intensity across countries over time
- **Country Comparison**: Compare pesticide trends among different countries
- **Overview Analysis**: Average vs latest year pesticide use comparison
- **Decade Analysis**: Pesticide use trends by decade with percentage changes
- **South Africa Focus**: Detailed analysis of South Africa's regional leadership
- **Pesticide Breakdown**: Analysis by pesticide types (herbicides, fungicides, insecticides)
- **Outlier Detection**: Identify unusual data points in the dataset

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/LordGeeOne/Pesticide-Use-Visualization---Data-Visualization-Assignment.git
   cd Pesticide-Use-Visualization---Data-Visualization-Assignment
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   # Create virtual environment
   python -m venv pesticide_env
   
   # Activate virtual environment
   # On Windows:
   pesticide_env\Scripts\activate
   
   # On macOS/Linux:
   source pesticide_env/bin/activate
   ```

3. **Install required packages**
   ```bash
   pip install streamlit pandas plotly matplotlib seaborn sqlite3
   ```

   Or install from requirements file:
   ```bash
   pip install -r requirements.txt
   ```

### Required Data Files

Ensure the following files are in the same directory as the dashboard:
- `Pesticide_Cleaned_Data_v3.csv` - Main dataset
- `Pesticide_Uses_ZA.db` - SQLite database for decade analysis

### Running the Dashboard

1. **Navigate to the Dashboard directory**
   ```bash
   cd Dashboard
   ```

2. **Run the Streamlit application**
   ```bash
   streamlit run Pesticide_Use_Dashboard.py
   ```

3. **Access the dashboard**
   - The dashboard will automatically open in your default web browser
   - If not, navigate to `http://localhost:8501`

## 📦 Dependencies

```txt
streamlit>=1.28.0
pandas>=1.5.0
plotly>=5.15.0
matplotlib>=3.6.0
seaborn>=0.12.0
sqlite3 (built-in with Python)
```

## 🗂️ Project Structure

```
Pesticide-Use-Visualization/
│
├── Dashboard/
│   └── Pesticide_Use_Dashboard.py    # Main dashboard application
│
├── Pesticide_Cleaned_Data_v3.csv     # Main dataset
├── Pesticide_Uses_ZA.db              # SQLite database
├── README.md                         # This file
└── requirements.txt                  # Python dependencies
```

## 💡 Usage

### Dashboard Navigation

Use the **sidebar** to:
- **Filter countries**: Select specific countries to analyze
- **Adjust year range**: Focus on specific time periods (1990-2023)
- **Choose pesticide types**: Filter by herbicides, fungicides, insecticides, or total
- **Navigate sections**: Switch between different analysis views

### Available Sections

1. **Regional Trends**: Overview of pesticide intensity trends
2. **Overview**: Side-by-side comparison of average vs latest year data
3. **Average by Decade**: Decade-wise analysis with growth percentages
4. **South Africa Leadership**: Detailed South Africa analysis
5. **Country Comparison**: Multi-country trend comparison
6. **Pesticides Breakdown**: Analysis by pesticide type
7. **Outliers Analysis**: Statistical outlier detection and visualization

## 🌍 Data Coverage

**Countries Included:**
- South Africa
- Zimbabwe
- Zambia
- Mozambique
- Namibia
- Botswana
- Lesotho
- Eswatini
- Angola
- Malawi

**Time Period:** 1990-2023

**Pesticide Types:**
- Herbicides
- Fungicides
- Insecticides
- Total pesticides

## 🔧 Troubleshooting

### Common Issues

1. **"streamlit command not found"**
   ```bash
   pip install streamlit
   ```

2. **Data files not found**
   - Ensure `Pesticide_Cleaned_Data_v3.csv` and `Pesticide_Uses_ZA.db` are in the correct directory
   - Check file paths in the code if you've moved files

3. **Package import errors**
   ```bash
   pip install --upgrade streamlit pandas plotly matplotlib seaborn
   ```

4. **Database connection issues**
   - Verify `Pesticide_Uses_ZA.db` exists and is not corrupted
   - Check file permissions

### Performance Tips

- For large datasets, consider filtering data before visualization
- Use the year range slider to focus on specific periods
- Select fewer countries for faster rendering

## 📈 Key Insights

- **South Africa leads** regional pesticide usage per hectare
- **Herbicides dominate** usage across all countries (~40%)
- **Pesticide intensity increased** significantly from 1990s to 2020s
- **Growth patterns vary** significantly between countries

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Data sources and methodology acknowledgments
- Streamlit community for excellent documentation
- Contributors and reviewers
