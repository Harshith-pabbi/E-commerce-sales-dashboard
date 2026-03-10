import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

# Set page config
st.set_page_config(page_title="E-Commerce Sales Dashboard", page_icon="🛒", layout="wide")

# Custom CSS for aesthetics
st.markdown("""
<style>
    .reportview-container .main .block-container{
        padding-top: 2rem;
    }
    h1 {
        color: #1E3A8A;
        font-family: 'Helvetica Neue', sans-serif;
    }
    h2, h3 {
        color: #374151;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .metric-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-title {
        color: #6B7280;
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .metric-value {
        color: #111827;
        font-size: 28px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    data_path = 'data/processed/cleaned_transactions.csv'
    if not os.path.exists(data_path):
        st.error(f"Data file not found at {data_path}. Please run `python src/process_data.py` first.")
        return pd.DataFrame()
    df = pd.read_csv(data_path)
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

if not df.empty:
    st.title("🛒 E-Commerce Sales Analytics Dashboard")
    st.markdown("Interactive overview of sales performance, revenue trends, and profitability.")
    st.divider()

    # --- Sidebar Filters ---
    st.sidebar.header("Filters")
    
    # Date Filter
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    start_date, end_date = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

    # Category Filter
    all_categories = df['category'].unique().tolist()
    selected_categories = st.sidebar.multiselect("Select Categories", all_categories, default=all_categories)

    # Region Filter
    all_regions = df['region'].unique().tolist()
    selected_regions = st.sidebar.multiselect("Select Regions", all_regions, default=all_regions)

    # --- Apply Filters ---
    mask = (
        (df['date'].dt.date >= start_date) & 
        (df['date'].dt.date <= end_date) &
        (df['category'].isin(selected_categories)) &
        (df['region'].isin(selected_regions))
    )
    filtered_df = df[mask]

    if filtered_df.empty:
        st.warning("No data found for the selected filters.")
    else:
        # --- Top Level KPIs ---
        total_revenue = filtered_df['revenue'].sum()
        total_profit = filtered_df['profit'].sum()
        total_orders = filtered_df['transaction_id'].nunique()
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        profit_margin = (total_profit / total_revenue) * 100 if total_revenue > 0 else 0

        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-title">Total Revenue</div><div class="metric-value">${total_revenue:,.0f}</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><div class="metric-title">Total Profit</div><div class="metric-value">${total_profit:,.0f}</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><div class="metric-title">Total Orders</div><div class="metric-value">{total_orders:,.0f}</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="metric-card"><div class="metric-title">Average Order Value</div><div class="metric-value">${avg_order_value:,.2f}</div></div>', unsafe_allow_html=True)

        st.divider()

        # --- Visualizations ---
        st.subheader("📈 Monthly Revenue & Profit Trends")
        
        # Monthly Trend Chart using Plotly
        monthly_trend = filtered_df.groupby('year_month')[['revenue', 'profit']].sum().reset_index()
        fig_trend = px.line(monthly_trend, x='year_month', y=['revenue', 'profit'], 
                            labels={'value': 'Amount ($)', 'year_month': 'Month', 'variable': 'Metric'},
                            color_discrete_map={'revenue': '#1E3A8A', 'profit': '#10B981'},
                            markers=True)
        fig_trend.update_layout(xaxis_tickangle=-45, legend_title="")
        st.plotly_chart(fig_trend, width='stretch')

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🏆 Top 10 Products by Revenue")
            top_products = filtered_df.groupby('product_id')['revenue'].sum().nlargest(10).reset_index()
            fig_products = px.bar(top_products, x='revenue', y='product_id', orientation='h',
                                  labels={'revenue': 'Revenue ($)', 'product_id': 'Product ID'},
                                  color='revenue', color_continuous_scale='Blues')
            fig_products.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_products, width='stretch')

        with col2:
            st.subheader("🌍 Profit by Region")
            region_profit = filtered_df.groupby('region')['profit'].sum().reset_index()
            fig_region = px.pie(region_profit, values='profit', names='region', 
                                hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_region, width='stretch')
            
        st.divider()
        
        st.subheader("📊 Category Performance Matrix")
        cat_performance = filtered_df.groupby('category').agg({
            'revenue': 'sum',
            'profit': 'sum',
            'quantity': 'sum'
        }).reset_index()
        
        fig_scatter = px.scatter(cat_performance, x='revenue', y='profit', size='quantity', color='category',
                                 hover_name='category', size_max=40,
                                 labels={'revenue': 'Total Revenue ($)', 'profit': 'Total Profit ($)'})
        st.plotly_chart(fig_scatter, width='stretch')

        # Raw Data Expander
        with st.expander("View Raw Data"):
            st.dataframe(filtered_df.head(100))
