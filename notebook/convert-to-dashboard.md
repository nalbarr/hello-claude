Convert `@EDA_refactored.ipynb` into a professional Streamlit dashboard with this exact layout.

## Layout Structure
- **Header**: Title + date range filter (applies globally)
  - Title: left
  - Date range filter: right
- **KPI Row**: 4 cards (Total Revenue, Monthly Growth, Average order value, Total Orders)
  - Trend indicators for Total Revenue, 
  - Use red for negative trends and green for positive trends
- **Charts Grid**: 2x2 layout
  - Revenue trend line chart:
    - solid line for current period
    - dashed line for the previous period
    - Add grid lines for easier reading
    - Y-axis formatting - show values as $300K instead of $300,000
  - Top 10 categories bar chart sorted descending:
    - Use blue gradient (light shade for lower values)
  - Bar chart showing satisfaction vs delivery time:
    - x-axis: Delivery time buckets (1-3 days, 4-7 days, etc.)
    - y-axis: Average review score
- **Bottom Row**: 2 cards
  - Average delivery time with trend indicator
  - Review Score:
    - Large number of stars
    - Subtitle: "Average Review Score"
 
## Key Requirements
- Use Plotly for all charts
- Professional styling with trend arrows/colors
- Do not use icons
- Use uniform card heights for each row
- Show two decimal places for each trend indicator
- Include requirements.txt and README.md
