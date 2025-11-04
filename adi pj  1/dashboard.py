import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="E-commerce Analytics Dashboard", layout="wide")

# Connect to database
@st.cache_data
def load_data():
    conn = sqlite3.connect('data/processed/ecommerce.db')

    # Load data
    customers = pd.read_sql_query("SELECT * FROM customers", conn)
    products = pd.read_sql_query("SELECT * FROM products", conn)
    orders = pd.read_sql_query("SELECT * FROM orders", conn)
    order_items = pd.read_sql_query("SELECT * FROM order_items", conn)

    conn.close()
    return customers, products, orders, order_items

def main():
    st.title("📊 E-commerce Analytics Dashboard")

    # Load data
    customers, products, orders, order_items = load_data()

    # Sidebar
    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Go to", ["Overview", "Sales Analysis", "Customer Insights", "Product Performance", "Geographic Analysis"])

    if page == "Overview":
        show_overview(customers, products, orders, order_items)
    elif page == "Sales Analysis":
        show_sales_analysis(orders, order_items)
    elif page == "Customer Insights":
        show_customer_insights(customers, orders)
    elif page == "Product Performance":
        show_product_performance(products, order_items)
    elif page == "Geographic Analysis":
        show_geographic_analysis(customers, orders)

def show_overview(customers, products, orders, order_items):
    st.header("📈 Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Customers", len(customers))

    with col2:
        st.metric("Total Products", len(products))

    with col3:
        st.metric("Total Orders", len(orders))

    with col4:
        total_revenue = orders['total_amount'].sum()
        st.metric("Total Revenue", f"${total_revenue:,.2f}")

    # Monthly sales trend
    st.subheader("Monthly Sales Trend")
    orders['order_date'] = pd.to_datetime(orders['order_date'])
    monthly_sales = orders.groupby(orders['order_date'].dt.to_period('M'))['total_amount'].sum().reset_index()
    monthly_sales['order_date'] = monthly_sales['order_date'].astype(str)

    fig = px.line(monthly_sales, x='order_date', y='total_amount', title="Monthly Revenue")
    st.plotly_chart(fig, use_container_width=True)

def show_sales_analysis(orders, order_items):
    st.header("💰 Sales Analysis")

    # Order status distribution
    st.subheader("Order Status Distribution")
    status_counts = orders['status'].value_counts()
    fig = px.pie(values=status_counts.values, names=status_counts.index, title="Order Status")
    st.plotly_chart(fig, use_container_width=True)

    # Top products
    st.subheader("Top 10 Best-Selling Products")
    top_products = order_items.groupby('product_id')['quantity'].sum().nlargest(10).reset_index()
    # Merge with product names
    conn = sqlite3.connect('data/processed/ecommerce.db')
    top_products = pd.read_sql_query("""
        SELECT p.product_id, p.name, SUM(oi.quantity) as total_quantity
        FROM products p
        JOIN order_items oi ON p.product_id = oi.product_id
        GROUP BY p.product_id, p.name
        ORDER BY total_quantity DESC
        LIMIT 10
    """, conn)
    conn.close()

    fig = px.bar(top_products, x='name', y='total_quantity', title="Top 10 Products by Quantity Sold")
    st.plotly_chart(fig, use_container_width=True)

def show_customer_insights(customers, orders):
    st.header("👥 Customer Insights")

    # Customer segmentation
    st.subheader("Customer Segmentation by Spending")
    customer_spending = orders.groupby('customer_id')['total_amount'].sum().reset_index()
    customer_spending = customer_spending.merge(customers[['customer_id', 'name']], on='customer_id')

    def categorize_spending(amount):
        if amount >= 5000:
            return 'High Value'
        elif amount >= 1000:
            return 'Medium Value'
        else:
            return 'Low Value'

    customer_spending['segment'] = customer_spending['total_amount'].apply(categorize_spending)
    segment_counts = customer_spending['segment'].value_counts()

    fig = px.pie(values=segment_counts.values, names=segment_counts.index, title="Customer Segments")
    st.plotly_chart(fig, use_container_width=True)

    # Top customers
    st.subheader("Top 10 Customers by Revenue")
    top_customers = customer_spending.nlargest(10, 'total_amount')
    fig = px.bar(top_customers, x='name', y='total_amount', title="Top Customers by Revenue")
    st.plotly_chart(fig, use_container_width=True)

def show_product_performance(products, order_items):
    st.header("📦 Product Performance")

    # Category performance
    st.subheader("Product Category Performance")
    conn = sqlite3.connect('data/processed/ecommerce.db')
    category_perf = pd.read_sql_query("""
        SELECT p.category, SUM(oi.quantity) as total_units, SUM(oi.item_total) as total_revenue
        FROM products p
        LEFT JOIN order_items oi ON p.product_id = oi.product_id
        GROUP BY p.category
        ORDER BY total_revenue DESC
    """, conn)
    conn.close()

    fig = px.bar(category_perf, x='category', y='total_revenue', title="Revenue by Category")
    st.plotly_chart(fig, use_container_width=True)

    # Inventory analysis
    st.subheader("Low Stock Products")
    low_stock = products[products['stock_quantity'] < 100].head(10)
    fig = px.bar(low_stock, x='name', y='stock_quantity', title="Low Stock Products")
    st.plotly_chart(fig, use_container_width=True)

def show_geographic_analysis(customers, orders):
    st.header("🌍 Geographic Analysis")

    # Sales by country
    st.subheader("Sales by Country")
    conn = sqlite3.connect('data/processed/ecommerce.db')
    geo_sales = pd.read_sql_query("""
        SELECT c.country, COUNT(o.order_id) as order_count, SUM(o.total_amount) as total_revenue
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.country
        ORDER BY total_revenue DESC
    """, conn)
    conn.close()

    fig = px.choropleth(geo_sales, locations='country', locationmode='country names',
                        color='total_revenue', title="Revenue by Country")
    st.plotly_chart(fig, use_container_width=True)

    # Country-wise metrics
    st.dataframe(geo_sales)

if __name__ == "__main__":
    main()
