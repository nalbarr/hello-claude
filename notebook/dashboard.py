import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings

from data_loader import load_and_process_data
from business_metrics import (
    calculate_revenue_metrics,
    calculate_monthly_growth_trend,
    calculate_average_order_value,
    calculate_order_count_metrics,
    calculate_product_category_performance,
    calculate_delivery_performance_metrics
)

warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="E-commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 0;
        color: #1f1f1f;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin: 0;
        margin-bottom: 0.5rem;
    }
    
    .metric-trend {
        font-size: 0.8rem;
        margin: 0;
    }
    
    .trend-positive {
        color: #28a745;
    }
    
    .trend-negative {
        color: #dc3545;
    }
    
    
    .bottom-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
    }
    
    .stSelectbox > div > div > div {
        background-color: white;
    }
    
    .stars {
        color: #ffc107;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_dashboard_data():
    """Load and cache data for dashboard"""
    try:
        loader, processed_data = load_and_process_data('ecommerce_data/')
        return loader, processed_data
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None


def format_currency(value):
    """Format currency values with K/M suffixes"""
    if abs(value) >= 1e6:
        return f"${value/1e6:.1f}M"
    elif abs(value) >= 1e3:
        return f"${value/1e3:.0f}K"
    else:
        return f"${value:.0f}"


def format_trend(current, previous):
    """Format trend indicators with arrows and colors"""
    if previous == 0:
        return "N/A"
    
    change_pct = ((current - previous) / previous) * 100
    arrow = "↗" if change_pct > 0 else "↘"
    color_class = "trend-positive" if change_pct > 0 else "trend-negative"
    
    return f'<span class="{color_class}">{arrow} {abs(change_pct):.2f}%</span>'


def create_revenue_trend_chart(current_data, previous_data, current_year, previous_year):
    """Create revenue trend line chart with solid/dashed lines and grid"""
    fig = go.Figure()
    
    # Group current year data by month
    current_monthly = current_data.groupby('month')['price'].sum().reset_index()
    
    # Current period - solid line
    fig.add_trace(go.Scatter(
        x=current_monthly['month'],
        y=current_monthly['price'],
        mode='lines+markers',
        name=f'{current_year}',
        line=dict(color='#007bff', width=3),  # Solid blue line
        marker=dict(size=8)
    ))
    
    # Previous period - dashed line
    if not previous_data.empty:
        previous_monthly = previous_data.groupby('month')['price'].sum().reset_index()
        fig.add_trace(go.Scatter(
            x=previous_monthly['month'],
            y=previous_monthly['price'],
            mode='lines+markers',
            name=f'{previous_year}',
            line=dict(color='#6c757d', width=2, dash='dash'),  # Dashed gray line
            marker=dict(size=6)
        ))
    
    fig.update_layout(
        title="Revenue Trend",
        xaxis_title="Month",
        yaxis_title="Revenue",
        showlegend=True,
        hovermode='x unified',
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(
            showgrid=True, 
            gridcolor='rgba(0,0,0,0.1)', 
            tickformat='$,.0s'  # Format as $300K instead of $300,000
        ),
        height=350,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig


def create_category_chart(sales_data):
    """Create top 10 categories bar chart sorted descending with blue gradient"""
    if 'product_category_name' not in sales_data.columns:
        return go.Figure().add_annotation(
            text="Product category data not available",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
        )
    
    category_revenue = sales_data.groupby('product_category_name')['price'].sum().sort_values(ascending=True).tail(10)
    
    # Create blue gradient (light shade for lower values)
    fig = go.Figure(data=[
        go.Bar(
            y=category_revenue.index,
            x=category_revenue.values,
            orientation='h',
            marker=dict(
                color=category_revenue.values,
                colorscale=[[0, '#E3F2FD'], [1, '#1976D2']],  # Light blue to dark blue
                showscale=False
            ),
            text=[format_currency(x) for x in category_revenue.values],
            textposition='outside',
            hovertemplate='%{y}<br>Revenue: %{text}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="Top 10 Categories",
        xaxis_title="Revenue",
        yaxis_title="",
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', tickformat='$,.0s'),
        yaxis=dict(showgrid=False, categoryorder='total ascending'),
        height=350,
        margin=dict(t=50, b=50, l=150, r=50)
    )
    
    return fig


def create_geographic_chart(sales_data):
    """Create top 10 states by revenue bar chart"""
    if 'customer_state' not in sales_data.columns:
        return go.Figure().add_annotation(
            text="Geographic data not available",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
        )
    
    # Get top 10 states by revenue
    state_revenue = sales_data.groupby('customer_state')['price'].sum().sort_values(ascending=True).tail(10)
    
    fig = go.Figure(data=[
        go.Bar(
            y=state_revenue.index,
            x=state_revenue.values,
            orientation='h',
            marker=dict(
                color=state_revenue.values,
                colorscale=[[0, '#FFF3E0'], [1, '#FF9800']],  # Light orange to dark orange
                showscale=False
            ),
            text=[format_currency(x) for x in state_revenue.values],
            textposition='outside',
            hovertemplate='%{y}<br>Revenue: %{text}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="Top 10 States by Revenue",
        xaxis_title="Revenue",
        yaxis_title="",
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', tickformat='$,.0s'),
        yaxis=dict(showgrid=False, categoryorder='total ascending'),
        height=350,
        margin=dict(t=50, b=50, l=100, r=50)
    )
    
    return fig


def create_state_map(sales_data):
    """Create US choropleth map"""
    if 'customer_state' not in sales_data.columns:
        return go.Figure().add_annotation(
            text="Geographic data not available",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
        )
    
    state_revenue = sales_data.groupby('customer_state')['price'].sum().reset_index()
    state_revenue.columns = ['state', 'revenue']
    
    fig = go.Figure(data=go.Choropleth(
        locations=state_revenue['state'],
        z=state_revenue['revenue'],
        locationmode='USA-states',
        colorscale='Blues',
        showscale=True,
        colorbar=dict(title="Revenue", tickformat='$,.0f')
    ))
    
    fig.update_layout(
        title="Revenue by State",
        geo_scope='usa',
        height=350,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig


def create_satisfaction_delivery_chart(sales_data):
    """Create satisfaction vs delivery time chart"""
    if 'delivery_days' not in sales_data.columns or 'review_score' not in sales_data.columns:
        return go.Figure().add_annotation(
            text="Delivery or review data not available",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
        )
    
    # Categorize delivery days
    def categorize_delivery(days):
        if pd.isna(days):
            return 'Unknown'
        elif days <= 3:
            return '1-3 days'
        elif days <= 7:
            return '4-7 days'
        else:
            return '8+ days'
    
    sales_data['delivery_category'] = sales_data['delivery_days'].apply(categorize_delivery)
    
    # Calculate average review score by delivery category
    delivery_satisfaction = sales_data.groupby('delivery_category')['review_score'].mean().reset_index()
    delivery_satisfaction = delivery_satisfaction[delivery_satisfaction['delivery_category'] != 'Unknown']
    
    # Order categories properly
    category_order = ['1-3 days', '4-7 days', '8+ days']
    delivery_satisfaction['delivery_category'] = pd.Categorical(
        delivery_satisfaction['delivery_category'], 
        categories=category_order, 
        ordered=True
    )
    delivery_satisfaction = delivery_satisfaction.sort_values('delivery_category')
    
    fig = go.Figure(data=[
        go.Bar(
            x=delivery_satisfaction['delivery_category'],
            y=delivery_satisfaction['review_score'],
            marker=dict(color='#1f77b4'),
            text=[f'{x:.2f}' for x in delivery_satisfaction['review_score']],
            textposition='outside',
        )
    ])
    
    fig.update_layout(
        title="Customer Satisfaction vs Delivery Time",
        xaxis_title="Delivery Time",
        yaxis_title="Average Review Score",
        plot_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', range=[0, 5]),
        height=350,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig


def main():
    """Main dashboard function"""
    
    # Load data
    loader, processed_data = load_dashboard_data()
    
    if loader is None:
        st.error("Failed to load data. Please check your data files.")
        return
    
    # Header with title and filters
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        st.title("📊 E-commerce Analytics Dashboard")
    
    with col2:
        # Year filter with default to 2023
        orders_data = processed_data['orders']
        available_years = sorted(orders_data['year'].unique(), reverse=True)
        
        default_year_index = 0
        if 2023 in available_years:
            default_year_index = available_years.index(2023)
        
        selected_year = st.selectbox(
            "Year",
            options=available_years,
            index=default_year_index,
            key="year_filter"
        )
    
    with col3:
        # Month filter
        month_options = ['All Months'] + [f'Month {i}' for i in range(1, 13)]
        selected_month_display = st.selectbox(
            "Month",
            options=month_options,
            index=0,
            key="month_filter"
        )
        
        selected_month = None if selected_month_display == 'All Months' else int(selected_month_display.split(' ')[1])
    
    with col4:
        # Date range filter (optional for advanced filtering)
        min_date = orders_data['order_purchase_timestamp'].min().date()
        max_date = orders_data['order_purchase_timestamp'].max().date()
        
        date_range = st.date_input(
            "Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key="date_filter"
        )
    
    # Create datasets based on selected filters
    current_data = loader.create_sales_dataset(
        year_filter=selected_year,
        month_filter=selected_month,
        status_filter='delivered'
    )
    
    # Apply additional date range filter if needed
    if len(date_range) == 2:
        start_date, end_date = date_range
        current_data = current_data[
            (current_data['order_purchase_timestamp'].dt.date >= start_date) &
            (current_data['order_purchase_timestamp'].dt.date <= end_date)
        ]
    
    # Set up comparison year data
    current_year = selected_year
    previous_year = selected_year - 1
    
    # Get previous year data with same month filter for comparison
    if previous_year in available_years:
        previous_data = loader.create_sales_dataset(
            year_filter=previous_year,
            month_filter=selected_month,
            status_filter='delivered'
        )
        
        # Apply same date range adjustment if needed
        if len(date_range) == 2:
            previous_data = previous_data[
                (previous_data['order_purchase_timestamp'].dt.date >= start_date.replace(year=previous_year)) &
                (previous_data['order_purchase_timestamp'].dt.date <= end_date.replace(year=previous_year))
            ]
    else:
        previous_data = pd.DataFrame()
    
    current_year_data = current_data
    
    # Import business_metrics functions
    from business_metrics import (
        calculate_revenue_metrics,
        calculate_monthly_growth_trend,
        calculate_average_order_value,
        calculate_order_count_metrics
    )
    
    # Calculate KPI metrics using business functions
    revenue_metrics = calculate_revenue_metrics(current_data, current_year, previous_year)
    order_metrics = calculate_order_count_metrics(current_data, current_year, previous_year)
    aov_metrics = calculate_average_order_value(current_data, current_year, previous_year)
    
    # Calculate monthly growth for current year
    monthly_growth = calculate_monthly_growth_trend(current_year_data, current_year)
    avg_monthly_growth = monthly_growth.mean() if len(monthly_growth) > 0 else 0
    
    # KPI Row - 4 cards with trend indicators (red for negative, green for positive)
    st.markdown("<br>", unsafe_allow_html=True)
    
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    def create_kpi_card(title, value, trend, is_percentage=False):
        trend_color = "#28a745" if trend >= 0 else "#dc3545"  # Green for positive, red for negative
        trend_arrow = "↗" if trend >= 0 else "↘"
        
        value_display = f"{value:.2f}%" if is_percentage else format_currency(value)
        
        return f"""
        <div class="metric-card">
            <p class="metric-label">{title}</p>
            <p class="metric-value">{value_display}</p>
            <p class="metric-trend" style="color: {trend_color};">
                <span style="font-size: 16px;">{trend_arrow}</span> {abs(trend):.2f}%
            </p>
        </div>
        """
    
    with kpi1:
        st.markdown(
            create_kpi_card("Total Revenue", revenue_metrics['current_revenue'], revenue_metrics['revenue_growth']),
            unsafe_allow_html=True
        )
    
    with kpi2:
        st.markdown(
            create_kpi_card("Monthly Growth", avg_monthly_growth, avg_monthly_growth, is_percentage=True),
            unsafe_allow_html=True
        )
    
    with kpi3:
        st.markdown(
            create_kpi_card("Average Order Value", aov_metrics['current_aov'], aov_metrics['aov_growth']),
            unsafe_allow_html=True
        )
    
    with kpi4:
        st.markdown(
            create_kpi_card("Total Orders", order_metrics['current_orders'], order_metrics['order_growth']),
            unsafe_allow_html=True
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Grid - 2x2 layout
    st.markdown("<br>", unsafe_allow_html=True)
    
    chart_row1_col1, chart_row1_col2 = st.columns(2)
    
    with chart_row1_col1:
        revenue_fig = create_revenue_trend_chart(current_year_data, previous_data, current_year, previous_year)
        st.plotly_chart(revenue_fig, use_container_width=True)
    
    with chart_row1_col2:
        category_fig = create_category_chart(current_year_data)
        st.plotly_chart(category_fig, use_container_width=True)
    
    chart_row2_col1, chart_row2_col2 = st.columns(2)
    
    with chart_row2_col1:
        satisfaction_fig = create_satisfaction_delivery_chart(current_year_data)
        st.plotly_chart(satisfaction_fig, use_container_width=True)
    
    with chart_row2_col2:
        # Geographic Performance Chart (Revenue by Top States)
        geographic_fig = create_geographic_chart(current_year_data)
        st.plotly_chart(geographic_fig, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bottom Row - 2 cards
    st.markdown("<br>", unsafe_allow_html=True)
    
    bottom_col1, bottom_col2 = st.columns(2)
    
    def create_bottom_card(title, value, subtitle="", is_stars=False):
        if is_stars:
            full_stars = int(value)
            stars = "★" * full_stars + "☆" * (5 - full_stars)
            value_display = f'<div style="font-size: 40px; color: #ffc107;">{stars}</div>'
            subtitle_display = f'<div style="font-size: 16px; color: #666; margin-top: 10px;">{subtitle}</div>'
        else:
            value_display = f'<div style="font-size: 32px; font-weight: bold; color: #333;">{value:.1f} days</div>'
            subtitle_display = f'<div style="font-size: 14px; color: #666; margin-top: 5px;">{subtitle}</div>' if subtitle else ""
        
        return f"""
        <div class="bottom-card">
            <div style="font-size: 16px; color: #333; font-weight: 600; margin-bottom: 15px;">{title}</div>
            {value_display}
            {subtitle_display}
        </div>
        """
    
    with bottom_col1:
        # Average delivery time with trend indicator
        if 'order_delivered_customer_date' in current_year_data.columns:
            # Calculate delivery days
            delivery_data = current_year_data.copy()
            delivery_data['delivery_days'] = (
                pd.to_datetime(delivery_data['order_delivered_customer_date']) - 
                pd.to_datetime(delivery_data['order_purchase_timestamp'])
            ).dt.days
            
            avg_delivery_days = delivery_data['delivery_days'].mean()
            
            st.markdown(
                create_bottom_card("Average Delivery Time", avg_delivery_days, "Days from order to delivery"),
                unsafe_allow_html=True
            )
        else:
            st.info("Delivery data not available")
    
    with bottom_col2:
        # Review Score with large stars
        if 'review_score' in current_year_data.columns:
            order_level_data = current_year_data.drop_duplicates('order_id')
            avg_review_score = order_level_data['review_score'].mean()
            
            st.markdown(
                create_bottom_card("Review Score", avg_review_score, "Average Review Score", is_stars=True),
                unsafe_allow_html=True
            )
        else:
            st.info("Review data not available")


if __name__ == "__main__":
    main()