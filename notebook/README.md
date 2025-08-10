# E-commerce Sales Analysis - Refactored

This project provides a comprehensive, well-structured approach to analyzing e-commerce sales performance data with improved code organization, enhanced visualizations, and configurable parameters.

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Launch Analysis**:
   ```bash
   jupyter notebook EDA_refactored.ipynb
   ```

3. **Launch Dashboard**:
   ```bash
   streamlit run dashboard.py
   ```

4. **Configure Analysis** (modify these parameters in the notebook):
   ```python
   CURRENT_YEAR = 2023          # Primary analysis year
   COMPARISON_YEAR = 2022       # Comparison baseline year
   ANALYSIS_MONTH = None        # Set to 1-12 for monthly analysis, None for full year
   ```

## Project Structure

```
├── EDA_refactored.ipynb       # Main refactored analysis notebook
├── dashboard.py              # Professional Streamlit dashboard
├── business_metrics.py        # Business metric calculation functions
├── data_loader.py            # Data loading and processing utilities
├── requirements.txt          # Python package dependencies
├── README.md                 # This documentation file
└── ecommerce_data/           # Data directory
    ├── orders_dataset.csv
    ├── order_items_dataset.csv
    ├── products_dataset.csv
    ├── customers_dataset.csv
    ├── order_reviews_dataset.csv
    └── order_payments_dataset.csv
```

## Key Features

### 🔧 **Configurable Analysis Framework**
- Flexible time periods (any year or specific month)
- Easy parameter configuration
- General-purpose metric calculations

### 📊 **Enhanced Visualizations**
- Business-oriented color schemes
- Clear titles with date ranges
- Interactive geographic maps
- Professional formatting (currency, percentages)

### 📈 **Comprehensive Business Metrics**
- **Revenue Analysis**: Growth rates and trends
- **Product Performance**: Category analysis and market share
- **Geographic Analysis**: State-level performance with US heatmap
- **Customer Experience**: Delivery performance and satisfaction
- **Operational Metrics**: Order fulfillment and status distribution

### 🏗️ **Improved Code Structure**
- **Modular Design**: Separate modules for metrics and data loading
- **Reusable Functions**: Well-documented functions with docstrings
- **Clean Organization**: Logical section structure with clear documentation

### 📱 **Professional Streamlit Dashboard**
- **Interactive KPI Cards**: Total Revenue, Monthly Growth, AOV, Total Orders with trend indicators
- **Revenue Trend Chart**: Solid line for current period, dashed for previous with grid lines
- **Top 10 Categories**: Horizontal bar chart with blue gradient, sorted descending
- **Satisfaction Analysis**: Customer satisfaction vs delivery time buckets
- **Customer Experience Cards**: Average delivery time and review score with stars
- **Global Date Filtering**: Apply date range filter across all dashboard metrics

## Analysis Sections

1. **Introduction & Business Objectives** - Context and KPI definitions
2. **Data Loading & Configuration** - Flexible parameter setup
3. **Data Preparation & Transformation** - Automated cleaning and validation
4. **Business Metrics Calculation** - Revenue, orders, products, geography
5. **Customer Experience Analysis** - Delivery and satisfaction metrics
6. **Summary of Key Observations** - Executive summary and recommendations

## Usage Examples

### Standard Annual Analysis
```python
CURRENT_YEAR = 2023
COMPARISON_YEAR = 2022
ANALYSIS_MONTH = None  # Full year
```

### Monthly Analysis
```python
CURRENT_YEAR = 2023
COMPARISON_YEAR = 2022
ANALYSIS_MONTH = 12  # December only
```

## Business Metrics Available

- Revenue growth and trends
- Average Order Value (AOV) analysis
- Product category performance
- Geographic revenue distribution
- Customer satisfaction scores
- Delivery performance metrics
- Order fulfillment rates

## Requirements

- Python 3.8+
- pandas, numpy, matplotlib, seaborn, plotly, streamlit
- Jupyter Notebook
- Complete ecommerce dataset in CSV format

## Data Quality

The analysis includes automated data quality assessment and handles missing data gracefully. Check the data quality section in the notebook for completeness metrics.

## Troubleshooting

**Import Errors**: `pip install -r requirements.txt`
**Data File Not Found**: Verify all CSV files are in `ecommerce_data/` directory
**Empty Results**: Check date filters and ensure data exists for specified periods