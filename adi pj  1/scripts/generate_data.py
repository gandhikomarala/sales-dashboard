import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Generate sample data for e-commerce simulation
def generate_customers(n=1000):
    customers = []
    for i in range(1, n+1):
        customer = {
            'customer_id': i,
            'name': f'Customer_{i}',
            'email': f'customer{i}@example.com',
            'age': random.randint(18, 80),
            'country': random.choice(['USA', 'UK', 'Canada', 'Germany', 'France', 'Australia']),
            'registration_date': datetime.now() - timedelta(days=random.randint(1, 365*2))
        }
        customers.append(customer)
    return pd.DataFrame(customers)

def generate_products(n=500):
    categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports', 'Beauty']
    products = []
    for i in range(1, n+1):
        product = {
            'product_id': i,
            'name': f'Product_{i}',
            'category': random.choice(categories),
            'price': round(random.uniform(10, 1000), 2),
            'stock_quantity': random.randint(0, 1000)
        }
        products.append(product)
    return pd.DataFrame(products)

def generate_orders(customers_df, products_df, n=5000):
    orders = []
    for i in range(1, n+1):
        customer = customers_df.sample(1).iloc[0]
        num_items = random.randint(1, 5)
        order_items = []
        total_amount = 0
        for _ in range(num_items):
            product = products_df.sample(1).iloc[0]
            quantity = random.randint(1, 10)
            item_total = product['price'] * quantity
            total_amount += item_total
            order_items.append({
                'product_id': product['product_id'],
                'quantity': quantity,
                'unit_price': product['price'],
                'item_total': item_total
            })

        order = {
            'order_id': i,
            'customer_id': customer['customer_id'],
            'order_date': datetime.now() - timedelta(days=random.randint(1, 365)),
            'total_amount': round(total_amount, 2),
            'status': random.choice(['Completed', 'Pending', 'Cancelled']),
            'items': order_items  # This will be handled separately for CSV
        }
        orders.append(order)
    return pd.DataFrame(orders)

if __name__ == "__main__":
    print("Generating sample e-commerce data...")

    # Generate data
    customers_df = generate_customers(1000)
    products_df = generate_products(500)
    orders_df = generate_orders(customers_df, products_df, 5000)

    # Save to CSV files
    customers_df.to_csv('data/raw/customers.csv', index=False)
    products_df.to_csv('data/raw/products.csv', index=False)
    orders_df.to_csv('data/raw/orders.csv', index=False)

    # For order items, create a separate CSV
    order_items = []
    for order in orders_df.itertuples():
        for item in order.items:
            order_items.append({
                'order_id': order.order_id,
                'product_id': item['product_id'],
                'quantity': item['quantity'],
                'unit_price': item['unit_price'],
                'item_total': item['item_total']
            })
    order_items_df = pd.DataFrame(order_items)
    order_items_df.to_csv('data/raw/order_items.csv', index=False)

    print("Sample data generated and saved to data/raw/")
    print(f"Customers: {len(customers_df)}")
    print(f"Products: {len(products_df)}")
    print(f"Orders: {len(orders_df)}")
    print(f"Order Items: {len(order_items_df)}")
