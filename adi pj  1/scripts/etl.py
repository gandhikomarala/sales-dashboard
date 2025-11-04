import pandas as pd
import sqlite3
import logging
from datetime import datetime
import os
from governance import enforce_data_governance

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_data():
    """Extract data from raw CSV files."""
    logger.info("Starting data extraction...")
    try:
        customers_df = pd.read_csv('data/raw/customers.csv')
        products_df = pd.read_csv('data/raw/products.csv')
        orders_df = pd.read_csv('data/raw/orders.csv')
        order_items_df = pd.read_csv('data/raw/order_items.csv')
        logger.info("Data extraction completed successfully.")
        return customers_df, products_df, orders_df, order_items_df
    except Exception as e:
        logger.error(f"Error during data extraction: {e}")
        raise

def transform_data(customers_df, products_df, orders_df, order_items_df):
    """Transform data: clean, handle missing values, aggregate metrics."""
    logger.info("Starting data transformation...")

    # Handle missing values
    customers_df = customers_df.dropna()
    products_df = products_df.dropna()
    orders_df = orders_df.dropna()
    order_items_df = order_items_df.dropna()

    # Convert date columns to datetime
    customers_df['registration_date'] = pd.to_datetime(customers_df['registration_date'])
    orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])

    # Add derived columns
    customers_df['age_group'] = pd.cut(customers_df['age'], bins=[0, 25, 35, 50, 100], labels=['18-25', '26-35', '36-50', '51+'])

    # Aggregate order metrics
    order_summary = orders_df.groupby('customer_id').agg({
        'total_amount': ['sum', 'mean', 'count'],
        'order_date': 'max'
    }).reset_index()
    order_summary.columns = ['customer_id', 'total_spent', 'avg_order_value', 'order_count', 'last_order_date']

    # Merge with customers
    customers_transformed = customers_df.merge(order_summary, on='customer_id', how='left')

    # Product performance
    product_performance = order_items_df.groupby('product_id').agg({
        'quantity': 'sum',
        'item_total': 'sum'
    }).reset_index()
    product_performance.columns = ['product_id', 'total_quantity_sold', 'total_revenue']

    products_transformed = products_df.merge(product_performance, on='product_id', how='left')

    # Fill NaN values with 0 for products with no sales
    products_transformed = products_transformed.fillna(0)

    logger.info("Data transformation completed successfully.")
    return customers_transformed, products_transformed, orders_df, order_items_df

def load_data(customers_df, products_df, orders_df, order_items_df):
    """Load transformed data to SQLite database (simulating S3 storage)."""
    logger.info("Starting data loading...")

    # Create processed directory if it doesn't exist
    os.makedirs('data/processed', exist_ok=True)

    # Save to CSV (simulating S3 upload)
    customers_df.to_csv('data/processed/customers_transformed.csv', index=False)
    products_df.to_csv('data/processed/products_transformed.csv', index=False)
    orders_df.to_csv('data/processed/orders_transformed.csv', index=False)
    order_items_df.to_csv('data/processed/order_items_transformed.csv', index=False)

    # Load to SQLite database
    conn = sqlite3.connect('data/processed/ecommerce.db')

    customers_df.to_sql('customers', conn, if_exists='replace', index=False)
    products_df.to_sql('products', conn, if_exists='replace', index=False)
    orders_df.to_sql('orders', conn, if_exists='replace', index=False)
    order_items_df.to_sql('order_items', conn, if_exists='replace', index=False)

    conn.close()

    logger.info("Data loading completed successfully.")

def run_etl():
    """Run the complete ETL process."""
    logger.info("Starting ETL process...")
    start_time = datetime.now()

    try:
        # Extract
        customers_df, products_df, orders_df, order_items_df = extract_data()

        # Transform
        customers_transformed, products_transformed, orders_transformed, order_items_transformed = transform_data(
            customers_df, products_df, orders_df, order_items_df
        )

        # Load
        load_data(customers_transformed, products_transformed, orders_transformed, order_items_transformed)

        # Data Governance Check
        logger.info("Running data governance checks...")
        governance_report = enforce_data_governance()

        end_time = datetime.now()
        duration = end_time - start_time
        logger.info(f"ETL process completed successfully in {duration}.")

    except Exception as e:
        logger.error(f"ETL process failed: {e}")
        raise

if __name__ == "__main__":
    run_etl()
