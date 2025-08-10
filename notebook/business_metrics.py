"""
Business Metrics Module for E-commerce Data Analysis

This module contains functions for calculating various business metrics
including revenue analysis, growth trends, customer experience metrics,
and product performance analysis. Functions are designed to be configurable
for different time periods and comparison analyses.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple


def calculate_revenue_metrics(
    sales_data: pd.DataFrame, 
    current_year: int = 2023, 
    comparison_year: int = 2022
) -> Dict[str, float]:
    """
    Calculate revenue metrics comparing current year vs previous year.
    
    Args:
        sales_data: DataFrame with delivered sales data containing 'year' and 'price' columns
        current_year: Year for current analysis (default: 2023)
        comparison_year: Year for comparison (default: 2022)
    
    Returns:
        Dictionary containing revenue metrics:
        - current_revenue: Total revenue for current year
        - previous_revenue: Total revenue for comparison year
        - revenue_growth: Revenue growth percentage
    """
    current_data = sales_data[sales_data['year'] == current_year]
    previous_data = sales_data[sales_data['year'] == comparison_year]
    
    current_revenue = current_data['price'].sum()
    previous_revenue = previous_data['price'].sum()
    
    if previous_revenue == 0:
        revenue_growth = 0
    else:
        revenue_growth = ((current_revenue - previous_revenue) / previous_revenue) * 100
    
    return {
        'current_revenue': current_revenue,
        'previous_revenue': previous_revenue,
        'revenue_growth': revenue_growth
    }


def calculate_monthly_growth_trend(sales_data: pd.DataFrame, year: int = 2023) -> pd.Series:
    """
    Calculate month-over-month growth trend for a specific year.
    
    Args:
        sales_data: DataFrame with sales data containing 'year', 'month', and 'price' columns
        year: Year to analyze (default: 2023)
    
    Returns:
        Series with monthly growth percentages
    """
    year_data = sales_data[sales_data['year'] == year]
    monthly_revenue = year_data.groupby('month')['price'].sum()
    monthly_growth = monthly_revenue.pct_change() * 100
    
    return monthly_growth


def calculate_average_order_value(
    sales_data: pd.DataFrame, 
    current_year: int = 2023, 
    comparison_year: int = 2022
) -> Dict[str, float]:
    """
    Calculate average order value metrics comparing current vs previous year.
    
    Args:
        sales_data: DataFrame with sales data containing 'year', 'order_id', and 'price' columns
        current_year: Year for current analysis (default: 2023)
        comparison_year: Year for comparison (default: 2022)
    
    Returns:
        Dictionary containing AOV metrics:
        - current_aov: Average order value for current year
        - previous_aov: Average order value for comparison year
        - aov_growth: AOV growth percentage
    """
    current_data = sales_data[sales_data['year'] == current_year]
    previous_data = sales_data[sales_data['year'] == comparison_year]
    
    current_aov = current_data.groupby('order_id')['price'].sum().mean()
    previous_aov = previous_data.groupby('order_id')['price'].sum().mean()
    
    if previous_aov == 0:
        aov_growth = 0
    else:
        aov_growth = ((current_aov - previous_aov) / previous_aov) * 100
    
    return {
        'current_aov': current_aov,
        'previous_aov': previous_aov,
        'aov_growth': aov_growth
    }


def calculate_order_count_metrics(
    sales_data: pd.DataFrame, 
    current_year: int = 2023, 
    comparison_year: int = 2022
) -> Dict[str, int]:
    """
    Calculate order count metrics comparing current vs previous year.
    
    Args:
        sales_data: DataFrame with sales data containing 'year' and 'order_id' columns
        current_year: Year for current analysis (default: 2023)
        comparison_year: Year for comparison (default: 2022)
    
    Returns:
        Dictionary containing order count metrics:
        - current_orders: Total orders for current year
        - previous_orders: Total orders for comparison year
        - order_growth: Order count growth percentage
    """
    current_data = sales_data[sales_data['year'] == current_year]
    previous_data = sales_data[sales_data['year'] == comparison_year]
    
    current_orders = current_data['order_id'].nunique()
    previous_orders = previous_data['order_id'].nunique()
    
    if previous_orders == 0:
        order_growth = 0
    else:
        order_growth = ((current_orders - previous_orders) / previous_orders) * 100
    
    return {
        'current_orders': current_orders,
        'previous_orders': previous_orders,
        'order_growth': order_growth
    }


def calculate_product_category_performance(
    sales_data: pd.DataFrame, 
    products_data: pd.DataFrame, 
    year: int = 2023
) -> pd.DataFrame:
    """
    Calculate revenue performance by product category for a specific year.
    
    Args:
        sales_data: DataFrame with sales data containing 'year', 'product_id', and 'price' columns
        products_data: DataFrame with product data containing 'product_id' and 'product_category_name'
        year: Year to analyze (default: 2023)
    
    Returns:
        DataFrame with product categories ranked by revenue
    """
    year_data = sales_data[sales_data['year'] == year]
    
    sales_categories = pd.merge(
        products_data[['product_id', 'product_category_name']],
        year_data[['product_id', 'price']]
    )
    
    category_performance = (
        sales_categories
        .groupby('product_category_name')['price']
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    
    return category_performance


def calculate_geographic_performance(
    sales_data: pd.DataFrame, 
    orders_data: pd.DataFrame,
    customers_data: pd.DataFrame,
    year: int = 2023
) -> pd.DataFrame:
    """
    Calculate revenue performance by state/geographic region.
    
    Args:
        sales_data: DataFrame with sales data containing 'order_id' and 'price'
        orders_data: DataFrame with order data containing 'order_id' and 'customer_id'
        customers_data: DataFrame with customer data containing 'customer_id' and 'customer_state'
        year: Year to analyze (default: 2023)
    
    Returns:
        DataFrame with states ranked by revenue
    """
    year_data = sales_data[sales_data['year'] == year]
    
    # Merge sales with customer data
    sales_customers = pd.merge(
        year_data[['order_id', 'price']], 
        orders_data[['order_id', 'customer_id']]
    )
    
    sales_states = pd.merge(
        sales_customers, 
        customers_data[['customer_id', 'customer_state']]
    )
    
    geographic_performance = (
        sales_states
        .groupby('customer_state')['price']
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    
    return geographic_performance


def calculate_delivery_performance_metrics(
    sales_data: pd.DataFrame, 
    reviews_data: pd.DataFrame,
    year: int = 2023
) -> Dict[str, float]:
    """
    Calculate delivery performance and customer satisfaction metrics.
    
    Args:
        sales_data: DataFrame with sales data containing delivery dates and timestamps
        reviews_data: DataFrame with review data containing 'order_id' and 'review_score'
        year: Year to analyze (default: 2023)
    
    Returns:
        Dictionary containing delivery performance metrics:
        - avg_delivery_days: Average delivery time in days
        - avg_review_score: Average customer review score
        - fast_delivery_score: Average review score for fast deliveries (1-3 days)
        - standard_delivery_score: Average review score for standard deliveries (4-7 days)
        - slow_delivery_score: Average review score for slow deliveries (8+ days)
    """
    year_data = sales_data[sales_data['year'] == year].copy()
    
    # Calculate delivery speed in days
    year_data['delivery_speed'] = (
        pd.to_datetime(year_data['order_delivered_customer_date']) - 
        pd.to_datetime(year_data['order_purchase_timestamp'])
    ).dt.days
    
    # Merge with reviews
    delivery_reviews = pd.merge(
        year_data[['order_id', 'delivery_speed']], 
        reviews_data[['order_id', 'review_score']]
    ).drop_duplicates()
    
    # Categorize delivery speed
    def categorize_delivery_speed(days):
        if days <= 3:
            return 'fast'
        elif days <= 7:
            return 'standard'
        else:
            return 'slow'
    
    delivery_reviews['delivery_category'] = delivery_reviews['delivery_speed'].apply(categorize_delivery_speed)
    
    # Calculate metrics
    avg_delivery_days = delivery_reviews['delivery_speed'].mean()
    avg_review_score = delivery_reviews['review_score'].mean()
    
    delivery_category_scores = delivery_reviews.groupby('delivery_category')['review_score'].mean()
    
    return {
        'avg_delivery_days': avg_delivery_days,
        'avg_review_score': avg_review_score,
        'fast_delivery_score': delivery_category_scores.get('fast', 0),
        'standard_delivery_score': delivery_category_scores.get('standard', 0),
        'slow_delivery_score': delivery_category_scores.get('slow', 0)
    }


def calculate_order_status_distribution(orders_data: pd.DataFrame, year: int = 2023) -> pd.Series:
    """
    Calculate the distribution of order statuses for a specific year.
    
    Args:
        orders_data: DataFrame with order data containing 'order_purchase_timestamp' and 'order_status'
        year: Year to analyze (default: 2023)
    
    Returns:
        Series with order status distribution as percentages
    """
    orders_data = orders_data.copy()
    orders_data['year'] = pd.to_datetime(orders_data['order_purchase_timestamp']).dt.year
    
    year_data = orders_data[orders_data['year'] == year]
    status_distribution = year_data['order_status'].value_counts(normalize=True) * 100
    
    return status_distribution


def filter_data_by_period(
    data: pd.DataFrame, 
    year: Optional[int] = None, 
    month: Optional[int] = None,
    date_column: str = 'order_purchase_timestamp'
) -> pd.DataFrame:
    """
    Filter data by configurable time period (year and/or month).
    
    Args:
        data: DataFrame to filter
        year: Year to filter by (optional)
        month: Month to filter by (optional)
        date_column: Column name containing the date/timestamp
    
    Returns:
        Filtered DataFrame
    """
    filtered_data = data.copy()
    
    # Ensure datetime conversion
    filtered_data[date_column] = pd.to_datetime(filtered_data[date_column])
    
    # Extract year and month for filtering
    filtered_data['filter_year'] = filtered_data[date_column].dt.year
    filtered_data['filter_month'] = filtered_data[date_column].dt.month
    
    # Apply filters
    if year is not None:
        filtered_data = filtered_data[filtered_data['filter_year'] == year]
    
    if month is not None:
        filtered_data = filtered_data[filtered_data['filter_month'] == month]
    
    # Clean up temporary columns
    filtered_data = filtered_data.drop(['filter_year', 'filter_month'], axis=1)
    
    return filtered_data


def generate_business_summary(
    sales_data: pd.DataFrame,
    products_data: pd.DataFrame, 
    orders_data: pd.DataFrame,
    customers_data: pd.DataFrame,
    reviews_data: pd.DataFrame,
    current_year: int = 2023,
    comparison_year: int = 2022,
    filter_month: Optional[int] = None
) -> Dict[str, any]:
    """
    Generate a comprehensive business performance summary.
    
    Args:
        sales_data: DataFrame with delivered sales data
        products_data: DataFrame with product data
        orders_data: DataFrame with order data
        customers_data: DataFrame with customer data
        reviews_data: DataFrame with review data
        current_year: Year for current analysis (default: 2023)
        comparison_year: Year for comparison (default: 2022)
        filter_month: Optional month filter (1-12)
    
    Returns:
        Dictionary containing comprehensive business metrics
    """
    # Apply month filter if specified
    if filter_month is not None:
        sales_data = filter_data_by_period(sales_data, month=filter_month)
        orders_data = filter_data_by_period(orders_data, month=filter_month)
    
    summary = {}
    
    # Revenue metrics
    summary['revenue'] = calculate_revenue_metrics(sales_data, current_year, comparison_year)
    
    # AOV metrics
    summary['aov'] = calculate_average_order_value(sales_data, current_year, comparison_year)
    
    # Order count metrics
    summary['orders'] = calculate_order_count_metrics(sales_data, current_year, comparison_year)
    
    # Monthly growth trend (only if not filtering by specific month)
    if filter_month is None:
        summary['monthly_growth'] = calculate_monthly_growth_trend(sales_data, current_year)
    
    # Product category performance
    summary['category_performance'] = calculate_product_category_performance(
        sales_data, products_data, current_year
    )
    
    # Geographic performance
    summary['geographic_performance'] = calculate_geographic_performance(
        sales_data, orders_data, customers_data, current_year
    )
    
    # Delivery performance
    summary['delivery_performance'] = calculate_delivery_performance_metrics(
        sales_data, reviews_data, current_year
    )
    
    # Order status distribution
    summary['order_status_distribution'] = calculate_order_status_distribution(
        orders_data, current_year
    )
    
    return summary