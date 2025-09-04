import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# --- Page Config ---
st.set_page_config(page_title="Pesticide Use in Southern Africa", layout="wide")

# Initialize session state
if 'countries_cleared' not in st.session_state:
    st.session_state.countries_cleared = False
if 'pesticides_cleared' not in st.session_state:
    st.session_state.pesticides_cleared = False

# Define sections for navigation
SECTIONS = [
    "Regional Trends",
    "Overview: Average vs Latest Year", 
    "Average Pesticide Use by Decade",
    "South Africa Regional Leadership",
    "Country Comparison",
    "Pesticides Breakdown",
    "Tonnes vs Kg/ha with Outliers",
]

# Short names for navigation buttons
SECTION_SHORT_NAMES = {
    "Regional Trends": "Regional Trends",
    "Overview: Average vs Latest Year": "Overview",
    "Average Pesticide Use by Decade": "By Decade",
    "South Africa Regional Leadership": "SA Leadership",
    "Country Comparison": "Country Comparison",
    "Pesticides Breakdown": "Pesticides",
    "Tonnes vs Kg/ha with Outliers": "Outliers",
}

# Navigation functions
def get_section_index(section_name):
    return SECTIONS.index(section_name) if section_name in SECTIONS else 0

def get_next_section(current_section):
    current_index = get_section_index(current_section)
    next_index = (current_index + 1) % len(SECTIONS)
    return SECTIONS[next_index]

def get_previous_section(current_section):
    current_index = get_section_index(current_section)
    prev_index = (current_index - 1) % len(SECTIONS)
    return SECTIONS[prev_index]

# Custom CSS for collapsible sidebar with icons
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" integrity="sha512-iecdLmaskl7CVkqkXNQ/ZH/XLlvWZOJyj7Yy7tcenmpD1ypASozpmT/E0iPtmFIB46ZmdtAc9eNBvH0H/ZpiBw==" crossorigin="anonymous">
<style>
    /* Import Font Awesome for icons with fallback */
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    /* Define brighter light green color palette */
    :root {
        --light-green: #20c997;
        --light-green-hover: #1aa085;
        --light-green-light: #c3f7e5;
        --light-green-border: #7ee3c7;
        --light-green-text: #0d7450;
    }
    
    /* Remove sidebar border completely */
    section[data-testid="stSidebar"] > div:first-child {
        border-right: none !important;
        border: none !important;
        padding: 1rem !important;
    }
    
    /* Custom sidebar styling with minimal padding */
    section[data-testid="stSidebar"] {
        width: 300px !important;
        transition: all 0.3s ease;
        padding: 0 !important;
    }
    
    /* Add minimal padding to sidebar content and minimize top space */
    section[data-testid="stSidebar"] > div {
        padding: 0.25rem 0.5rem 0.5rem 0.5rem !important;
        padding-top: 0.25rem !important;
    }
    
    /* Collapsed sidebar styling */
    section[data-testid="stSidebar"][aria-expanded="false"] {
        width: 80px !important;
        min-width: 80px !important;
    }
    
    /* Remove left padding from expand/collapse toggle when sidebar is collapsed */
    section[data-testid="stSidebar"][aria-expanded="false"] button[kind="header"] {
        padding-left: 0 !important;
        margin-left: 0 !important;
    }
    
    /* Also target the collapse button specifically */
    section[data-testid="stSidebar"][aria-expanded="false"] button[data-testid*="baseButton"] {
        padding-left: 0 !important;
        margin-left: 0 !important;
    }
    
    /* Force show icons when collapsed by using different approach */
    .sidebar-icon-container {
        display: none;
    }
    
    /* Show icon container when sidebar is collapsed */
    section[data-testid="stSidebar"][aria-expanded="false"] .sidebar-icon-container {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        padding: 20px 10px !important;
        width: 100% !important;
        position: relative !important;
        top: 0 !important;
        left: 0 !important;
        background: inherit !important;
        box-shadow: none !important;
        backdrop-filter: none !important;
    }
    
    /* Hide all other content when collapsed */
    section[data-testid="stSidebar"][aria-expanded="false"] .element-container:not(:has(.sidebar-icon-container)),
    section[data-testid="stSidebar"][aria-expanded="false"] .stMarkdown:not(:has(.sidebar-icon-container)) {
        display: none !important;
    }
    
    /* Individual icon styling - Light Green Theme */
    .sidebar-icon {
        font-size: 18px;
        margin: 10px 0;
        text-align: center;
        padding: 12px;
        border-radius: 8px;
        background-color: var(--light-green-light);
        color: var(--light-green-text);
        transition: all 0.3s ease;
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        border: 1px solid var(--light-green-border);
        position: relative;
    }
    
    .sidebar-icon:hover {
        background-color: var(--light-green);
        color: white;
        transform: scale(1.05);
        box-shadow: 0 2px 8px rgba(40, 167, 69, 0.3);
    }
    
    .sidebar-icon i {
        font-size: 16px;
    }
    
    /* Tooltip styling */
    .sidebar-icon::after {
        content: attr(title);
        position: absolute;
        left: 60px;
        top: 50%;
        transform: translateY(-50%);
        background: var(--light-green-text);
        color: white;
        padding: 6px 10px;
        border-radius: 4px;
        font-size: 11px;
        white-space: nowrap;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.3s ease;
        z-index: 1000;
        font-family: "Source Sans Pro", sans-serif;
    }
    
    .sidebar-icon:hover::after {
        opacity: 1;
    }
    
    /* Tooltip arrow */
    .sidebar-icon::before {
        content: "";
        position: absolute;
        left: 55px;
        top: 50%;
        transform: translateY(-50%);
        border: 5px solid transparent;
        border-right-color: var(--light-green-text);
        opacity: 0;
        transition: opacity 0.3s ease;
        z-index: 1001;
    }
    
    .sidebar-icon:hover::before {
        opacity: 1;
    }
    
    /* Enhanced button styling with light green accent */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        border: 1px solid var(--light-green-border);
        background-color: var(--light-green-light);
        color: var(--light-green-text);
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        background-color: var(--light-green);
        border-color: var(--light-green-hover);
        color: white;
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(32, 201, 151, 0.2);
    }
    
    /* Clear button styling - smaller and green */
    .stButton[data-testid*="clear"] > button,
    button[kind="secondary"] {
        width: 20px !important;
        height: 20px !important;
        min-height: 20px !important;
        padding: 0 !important;
        border-radius: 50% !important;
        background-color: var(--light-green) !important;
        border: 1px solid var(--light-green-hover) !important;
        color: white !important;
        font-size: 10px !important;
        font-weight: bold !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 !important;
        margin-top: 2px !important;
    }
    
    .stButton[data-testid*="clear"] > button:hover,
    button[kind="secondary"]:hover {
        background-color: var(--light-green-hover) !important;
        border-color: var(--light-green-text) !important;
        transform: scale(1.1) !important;
        box-shadow: 0 2px 6px rgba(32, 201, 151, 0.3) !important;
    }
    
    /* Hide only the "clear all" buttons, keep individual item X buttons */
    .stMultiSelect div[data-baseweb="select"] button[aria-label*="Clear all"] {
        display: none !important;
    }
    
    .stMultiSelect div[data-baseweb="select"] button[title*="Clear all"] {
        display: none !important;
    }
    
    .stMultiSelect div[data-baseweb="select"] button[aria-label*="clear all"] {
        display: none !important;
    }
    
    .stMultiSelect div[data-baseweb="select"] button[title*="clear all"] {
        display: none !important;
    }
    
    /* Hide clear all button in multiselect dropdown menu */
    .stMultiSelect div[data-baseweb="popover"] button[aria-label*="Clear all"],
    .stMultiSelect div[data-baseweb="popover"] button[title*="Clear all"] {
        display: none !important;
    }
    
    /* Keep individual item X buttons visible and style them green */
    .stMultiSelect span[data-baseweb="tag"] button {
        background-color: var(--light-green) !important;
        color: white !important;
        border: none !important;
        border-radius: 50% !important;
        width: 16px !important;
        height: 16px !important;
        font-size: 10px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.2s ease !important;
    }
    
    .stMultiSelect span[data-baseweb="tag"] button:hover {
        background-color: var(--light-green-hover) !important;
        transform: scale(1.1) !important;
    }
    
    /* Style the multiselect tags to match green theme */
    .stMultiSelect span[data-baseweb="tag"] {
        background-color: var(--light-green-light) !important;
        color: var(--light-green-text) !important;
        border: 1px solid var(--light-green-border) !important;
        border-radius: 16px !important;
        padding: 2px 8px !important;
    }
    
    /* Hide the main clear indicator (X on the right side of multiselect) */
    .stMultiSelect .css-tlfecz-indicatorContainer:last-child {
        display: none !important;
    }
    
    .stMultiSelect div[data-baseweb="select"] > div > div:last-child button {
        display: none !important;
    }
    
    /* More selective hiding - only target main clear buttons */
    .stMultiSelect [role="button"][aria-label*="clear all"],
    .stMultiSelect [role="button"][aria-label*="Clear all"],
    .stMultiSelect [role="button"][title*="clear all"],
    .stMultiSelect [role="button"][title*="Clear all"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }
    
    /* Sidebar headers with light green icons */
    .sidebar-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 10px;
        font-size: 16px;
        color: var(--light-green-text);
        font-weight: 600;
    }
    
    .sidebar-header i {
        color: var(--light-green);
    }
    
    /* Filter inputs styling - Light Green Theme */
    .stSelectbox > div > div > div,
    .stMultiSelect > div > div > div {
        border-color: var(--light-green-border) !important;
        border-radius: 6px !important;
    }
    
    .stSelectbox > div > div > div:focus-within,
    .stMultiSelect > div > div > div:focus-within {
        border-color: var(--light-green) !important;
        box-shadow: 0 0 0 0.2rem rgba(40, 167, 69, 0.25) !important;
    }
    
    /* Multiselect tags styling */
    .stMultiSelect span[data-baseweb="tag"] {
        background-color: var(--light-green-light) !important;
        color: var(--light-green-text) !important;
        border: 1px solid var(--light-green-border) !important;
    }
    
    .stMultiSelect span[data-baseweb="tag"] span[title] {
        color: var(--light-green-text) !important;
    }
    
    /* Slider styling - Accent green theme with fallbacks */
    .stSlider > div > div > div > div,
    .stSlider div[data-baseweb="slider"] > div > div > div {
        background-color: var(--light-green-light) !important;
    }
    
    .stSlider > div > div > div > div > div,
    .stSlider div[data-baseweb="slider"] > div > div > div > div {
        
    }
    
    .stSlider > div > div > div > div > div > div,
    .stSlider div[data-baseweb="slider"] > div > div > div > div > div {
        background-color: var(--light-green) !important;
        border: 2px solid white !important;
        box-shadow: 0 0 0 2px var(--light-green) !important;
    }
    
    /* Slider track styling */
    .stSlider div[data-baseweb="slider"] div[data-testid="stSlider"] > div > div > div {
        background-color: var(--light-green-light) !important;
    }
    
    /* Active/filled portion of slider track */
    .stSlider div[data-baseweb="slider"] div[data-testid="stSlider"] > div > div > div > div {
        background-color: var(--light-green) !important;
    }
    
    /* Slider thumbs/handles */
    .stSlider div[data-baseweb="slider"] div[data-testid="stSlider"] > div > div > div > div > div {
        background-color: var(--light-green) !important;
        border: 2px solid white !important;
        box-shadow: 0 0 0 2px var(--light-green), 0 2px 4px rgba(32, 201, 151, 0.3) !important;
    }
    
    /* Slider thumb hover state */
    .stSlider div[data-baseweb="slider"] div[data-testid="stSlider"] > div > div > div > div > div:hover {
        background-color: var(--light-green-hover) !important;
        box-shadow: 0 0 0 3px var(--light-green-hover), 0 3px 6px rgba(32, 201, 151, 0.4) !important;
        transform: scale(1.1) !important;
    }
    
    /* Slider labels and values - accent green text */
    .stSlider .stMarkdown,
    .stSlider .stMarkdown p {
        color: var(--light-green-text) !important;
        font-weight: 500 !important;
    }
    
    /* Plain green text for slider range values */
    .stSlider div[data-testid="stMarkdownContainer"] p {
        color: var(--light-green-text) !important;
        font-weight: 500 !important;
        border: none !important;
        background: none !important;
        box-shadow: none !important;
    }
    
    /* Cross-browser slider input styling */
    .stSlider input[type="range"] {
        background: transparent !important;
        outline: none !important;
    }
    
    .stSlider input[type="range"]::-webkit-slider-track {
        background: var(--light-green-light) !important;
        border-radius: 4px !important;
        height: 6px !important;
    }
    
    .stSlider input[type="range"]::-webkit-slider-thumb {
        background: var(--light-green) !important;
        border: 2px solid white !important;
        border-radius: 50% !important;
        box-shadow: 0 0 0 1px var(--light-green) !important;
        cursor: pointer !important;
        height: 20px !important;
        width: 20px !important;
        -webkit-appearance: none !important;
    }
    
    .stSlider input[type="range"]::-moz-range-track {
        background: var(--light-green-light) !important;
        border-radius: 4px !important;
        height: 6px !important;
        border: none !important;
    }
    
    .stSlider input[type="range"]::-moz-range-thumb {
        background: var(--light-green) !important;
        border: 2px solid white !important;
        border-radius: 50% !important;
        box-shadow: 0 0 0 1px var(--light-green) !important;
        cursor: pointer !important;
        height: 20px !important;
        width: 20px !important;
        -moz-appearance: none !important;
    }
    
    /* Section headers - reverted to original format */
    h2, h3 {
        color: inherit !important;
    }
    
    /* Metric containers with light green accent */
    div[data-testid="metric-container"] {
        border-left: 4px solid var(--light-green) !important;
        padding-left: 1rem !important;
        background-color: rgba(40, 167, 69, 0.05) !important;
        border-radius: 0 8px 8px 0 !important;
    }
    
    /* Main content area adjustment */
    .main .block-container {
        padding-top: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    /* Collapsed sidebar main content adjustment */
    section[data-testid="stSidebar"][aria-expanded="false"] ~ .main .block-container {
        margin-left: 0;
        max-width: calc(100% - 80px);
    }
    
    /* Hide scrollbar for sidebar while keeping scrolling functionality */
    section[data-testid="stSidebar"] > div {
        scrollbar-width: none; /* Firefox */
        -ms-overflow-style: none; /* Internet Explorer 10+ */
    }
    
    section[data-testid="stSidebar"] > div::-webkit-scrollbar {
        display: none; /* WebKit browsers */
    }
    
    /* Fix multiselect and other inputs spacing */
    .stMultiSelect, .stSelectbox, .stSlider {
        margin-bottom: 1rem;
    }
    
    /* Ensure proper spacing */
    .element-container {
        margin-bottom: 0.5rem;
    }
    
    /* Divider styling */
    hr {
        border-color: var(--light-green-light) !important;
        margin: 1.5rem 0 !important;
    }
    
    /* Chart containers with subtle light green border */
    .stPlotlyChart, .stPyplot {
        border: 1px solid var(--light-green-light);
        border-radius: 8px;
        padding: 0.5rem;
        background-color: rgba(40, 167, 69, 0.02);
    }
    
    /* Navigation button text wrapping fix - more specific selectors */
    div[data-testid="column"] .stButton > button {
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        min-width: 120px !important;
        max-width: 100% !important;
        font-size: 0.85rem !important;
        padding: 0.375rem 0.75rem !important;
        height: auto !important;
        line-height: 1.2 !important;
    }
    
    /* Force horizontal layout for navigation buttons */
    .stButton button {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        flex-direction: row !important;
        white-space: nowrap !important;
        width: 100% !important;
        border-radius: 0 !important;
        border: 1px solid var(--light-green) !important;
    }
    
    /* Ensure proper alignment of navigation elements */
    div[data-testid="column"]:has(.stButton) {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌍 Pesticide Use in Southern Africa (1990–2023)")

# --- Load CSV Data with error handling ---
try:
    data = pd.read_csv("Pesticide_Cleaned_Data_v3.csv")
    if data.empty:
        st.error("❌ The data file is empty. Please check the CSV file.")
        st.stop()
except FileNotFoundError:
    st.error("❌ Data file 'Pesticide_Cleaned_Data_v3.csv' not found. Please ensure the file is in the correct directory.")
    st.stop()
except Exception as e:
    st.error(f"❌ Error loading data: {str(e)}")
    st.stop()

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

# --- Sidebar Navigation & Filters ---
# Add collapsible sidebar toggle
with st.sidebar:
    # Sidebar icons for collapsed state - shown as vertical column when collapsed
    st.markdown("""
    <div class="sidebar-icon-container">
        <div class="sidebar-icon" title="Navigation">
            <i class="fas fa-compass"></i>
        </div>
        <div class="sidebar-icon" title="Countries">
            <i class="fas fa-globe-africa"></i>
        </div>
        <div class="sidebar-icon" title="Pesticide Types">
            <i class="fas fa-flask"></i>
        </div>
        <div class="sidebar-icon" title="Time Range">
            <i class="fas fa-calendar-alt"></i>
        </div>
    </div>
    
    <script>
    // JavaScript to handle sidebar collapse detection
    function handleSidebarCollapse() {
        const sidebar = document.querySelector('section[data-testid="stSidebar"]');
        const iconContainer = document.querySelector('.sidebar-icon-container');
        
        if (sidebar && iconContainer) {
            const observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    if (mutation.type === 'attributes' && mutation.attributeName === 'aria-expanded') {
                        const isExpanded = sidebar.getAttribute('aria-expanded') === 'true';
                        if (isExpanded) {
                            iconContainer.style.display = 'none';
                        } else {
                            iconContainer.style.display = 'flex';
                            iconContainer.style.flexDirection = 'column';
                            iconContainer.style.alignItems = 'center';
                        }
                    }
                });
            });
            
            observer.observe(sidebar, { attributes: true });
        }
    }
    
    // Wait for DOM to load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', handleSidebarCollapse);
    } else {
        handleSidebarCollapse();
    }
    
    // Also try after a short delay in case Streamlit takes time to render
    setTimeout(handleSidebarCollapse, 1000);
    </script>
    """, unsafe_allow_html=True)
    
    # Navigation Section
    st.markdown('<div class="sidebar-header"><i class="fas fa-compass"></i> <strong>Dashboard Navigation</strong></div>', unsafe_allow_html=True)

    # Section Selection (at the top)
    # Initialize section in session state if not present
    if 'current_section' not in st.session_state:
        st.session_state.current_section = SECTIONS[0]
    
    # Handle navigation from buttons
    if 'section_nav' in st.session_state and st.session_state.section_nav:
        st.session_state.current_section = st.session_state.section_nav
        st.session_state.section_nav = None
    
    # Section selectbox that reflects the current section
    section = st.selectbox(
        "Select Section",
        SECTIONS,
        index=SECTIONS.index(st.session_state.current_section),
        label_visibility="collapsed",
        key="section_selector"
    )
    
    # Update session state when selectbox changes
    if section != st.session_state.current_section:
        st.session_state.current_section = section

    st.markdown("---")
    
    # Filters Section
    st.markdown('<div class="sidebar-header"><i class="fas fa-filter"></i> <strong>Filters</strong></div>', unsafe_allow_html=True)

    # Country Filters (second) with Clear All button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<i class="fas fa-globe-africa"></i> **Countries**', unsafe_allow_html=True)
    with col2:
        if st.button("✕", key="clear_countries", help="Clear all countries"):
            st.session_state.countries_cleared = True
    
    # Check if clear button was pressed
    default_countries = list(data["Country"].unique()) if not st.session_state.get('countries_cleared', False) else []
    if st.session_state.get('countries_cleared', False):
        st.session_state.countries_cleared = False
    
    selected_countries = st.multiselect(
        "Select countries to display",
        options=sorted(data["Country"].unique()),
        default=default_countries,
        label_visibility="collapsed"
    )

    # Pesticide Features (third) with Clear All button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<i class="fas fa-flask"></i> **Pesticide Types**', unsafe_allow_html=True)
    with col2:
        if st.button("✕", key="clear_pesticides", help="Clear all pesticide types"):
            st.session_state.pesticides_cleared = True
    
    # Check if clear button was pressed
    default_pesticides = list(data["Pesticide_Type"].unique()) if not st.session_state.get('pesticides_cleared', False) else []
    if st.session_state.get('pesticides_cleared', False):
        st.session_state.pesticides_cleared = False
    
    selected_types = st.multiselect(
        "Select Pesticide Types",
        options=data["Pesticide_Type"].unique(),
        default=default_pesticides,
        label_visibility="collapsed"
    )

    # Year Filter (last)
    st.markdown('<i class="fas fa-calendar-alt"></i> **Year Range**', unsafe_allow_html=True)
    year_range = st.slider(
        "Select Year Range",
        int(data["Year"].min()),
        int(data["Year"].max()),
        (1990, 2023),
        step=1,
        label_visibility="collapsed"
    )

# Filter data based on selections with safety checks
if selected_countries and selected_types:
    filtered_data = data[
        (data["Country"].isin(selected_countries)) &
        (data["Year"] >= year_range[0]) &
        (data["Year"] <= year_range[1]) &
        (data["Pesticide_Type"].isin(selected_types))
    ]
else:
    # If no countries or pesticide types selected, show empty dataframe
    filtered_data = pd.DataFrame()

# Check if filtered data is empty
if filtered_data.empty:
    st.warning("⚠️ No data available for the selected filters. Please adjust your selection.")
    st.stop()

# Navigation function
def create_navigation_buttons(current_section):
    """Create navigation buttons for section navigation"""
    current_index = get_section_index(current_section)
    prev_section = get_previous_section(current_section)
    next_section = get_next_section(current_section)
    
    # Get short names for buttons
    prev_short = SECTION_SHORT_NAMES.get(prev_section, prev_section)
    next_short = SECTION_SHORT_NAMES.get(next_section, next_section)
    
    # Create navigation with proper spacing
    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
    
    # Create properly justified columns with specific proportions
    col1, col2, col3 = st.columns([3, 2, 3])
    
    with col1:
        if st.button(f"← {prev_short}", key=f"prev_{current_section}", help=f"Go to {prev_section}", use_container_width=True):
            st.session_state.section_nav = prev_section
            st.rerun()
    
    with col2:
        st.markdown(f"<div style='text-align: center; padding: 0.75rem; color: var(--light-green-text); font-weight: 600; font-size: 1rem; display: flex; align-items: center; justify-content: center; height: 2.5rem;'>{current_index + 1}/{len(SECTIONS)}</div>", unsafe_allow_html=True)
    
    with col3:
        if st.button(f"{next_short} →", key=f"next_{current_section}", help=f"Go to {next_section}", use_container_width=True):
            st.session_state.section_nav = next_section
            st.rerun()
    
    st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)

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
    
    # Navigation buttons
    create_navigation_buttons(section)

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
    
    # Navigation buttons
    create_navigation_buttons(section)

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
    
    # Navigation buttons
    create_navigation_buttons(section)

# -----------------------
# Section: Average Pesticide Use by Decade
# -----------------------
elif section == "Average Pesticide Use by Decade":
    st.subheader("📊 Average Pesticide Use per Hectare by Decade")
    
    # Use filtered CSV data instead of database
    df_db = filtered_data.copy()

    def get_decade(year):
        if 1990 <= year <= 1999: return "1990s"
        elif 2000 <= year <= 2009: return "2000s"
        elif 2010 <= year <= 2019: return "2010s"
        elif 2020 <= year <= 2023: return "2020s"
        else: return "Other"

    df_db["Decade"] = df_db["Year"].apply(get_decade)
    avg_decade = df_db.groupby("Decade", as_index=False)["Kg_per_ha"].mean().rename(columns={"Kg_per_ha":"Avg_Kg_per_ha"})
    st.dataframe(avg_decade)

    if len(avg_decade) > 1:
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
    
    # Navigation buttons
    create_navigation_buttons(section)

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
    
    # Navigation buttons
    create_navigation_buttons(section)

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
        
        # Navigation buttons
        create_navigation_buttons(section)

# Section: Tonnes vs Kg/ha with Outliers
elif section == "Tonnes vs Kg/ha with Outliers":
    st.subheader("📉 Tonnes vs Kg per Hectare with Outliers Highlighted")
    df = filtered_data[filtered_data["Pesticide_Type"] != "Pesticides (total)"].copy()
    Q1 = df["Kg_per_ha"].quantile(0.25)
    Q3 = df["Kg_per_ha"].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[(df["Kg_per_ha"] < (Q1 - 1.5*IQR)) | (df["Kg_per_ha"] > (Q3 + 1.5*IQR))]

    fig8, ax = plt.subplots(figsize=(10,6))
    sns.scatterplot(x="Tonnes", y="Kg_per_ha", hue="Pesticide_Type", data=df, palette="Set2", ax=ax)
    ax.scatter(outliers["Tonnes"], outliers["Kg_per_ha"], color="red", label="Outliers", s=60, edgecolor="black")
    ax.set_title("Tonnes vs Kg per Hectare with Outliers Highlighted", fontsize=16, fontweight='bold')
    ax.set_xlabel("Tonnes", fontsize=14)
    ax.set_ylabel("Kg per Ha", fontsize=14)
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    st.pyplot(fig8)
    st.write(f"**Correlation:** {df['Tonnes'].corr(df['Kg_per_ha']):.3f}")
    st.write(f"**Number of detected outliers:** {len(outliers)}")
    st.dataframe(outliers)
    
    # Navigation buttons
    create_navigation_buttons(section)
