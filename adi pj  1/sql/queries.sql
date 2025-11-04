-- SQL Queries for E-commerce Data Analysis

-- 1. Total Sales and Revenue Overview
SELECT
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT c.customer_id) AS total_customers,
    COUNT(DISTINCT p.product_id) AS total_products,
    SUM(o.total_amount) AS total_revenue,
    AVG(o.total_amount) AS avg_order_value
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON 1=1;  -- Cross join for product count

-- 2. Top 10 Best-Selling Products
SELECT
    p.product_id,
    p.name,
    p.category,
    SUM(oi.quantity) AS total_quantity_sold,
    SUM(oi.item_total) AS total_revenue,
    AVG(oi.unit_price) AS avg_selling_price
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.name, p.category
ORDER BY total_quantity_sold DESC
LIMIT 10;

-- 3. Customer Segmentation by Spending
SELECT
    CASE
        WHEN total_spent >= 5000 THEN 'High Value'
        WHEN total_spent >= 1000 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS customer_segment,
    COUNT(*) AS customer_count,
    AVG(total_spent) AS avg_spending,
    SUM(total_spent) AS total_segment_revenue
FROM (
    SELECT
        c.customer_id,
        COALESCE(SUM(o.total_amount), 0) AS total_spent
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id
) customer_spending
GROUP BY customer_segment;

-- 4. Monthly Sales Trend
SELECT
    strftime('%Y-%m', order_date) AS month,
    COUNT(DISTINCT order_id) AS orders_count,
    SUM(total_amount) AS monthly_revenue,
    AVG(total_amount) AS avg_order_value
FROM orders
GROUP BY strftime('%Y-%m', order_date)
ORDER BY month;

-- 5. Product Category Performance
SELECT
    p.category,
    COUNT(DISTINCT p.product_id) AS products_in_category,
    SUM(oi.quantity) AS total_units_sold,
    SUM(oi.item_total) AS total_category_revenue,
    AVG(oi.item_total / oi.quantity) AS avg_product_price
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY total_category_revenue DESC;

-- 6. Customer Lifetime Value Analysis
SELECT
    c.customer_id,
    c.name,
    c.age_group,
    c.country,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_spent,
    AVG(o.total_amount) AS avg_order_value,
    MAX(o.order_date) AS last_order_date,
    julianday('now') - julianday(MAX(o.order_date)) AS days_since_last_order
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.age_group, c.country
ORDER BY total_spent DESC;

-- 7. Order Status Distribution
SELECT
    status,
    COUNT(*) AS order_count,
    SUM(total_amount) AS total_amount,
    AVG(total_amount) AS avg_amount
FROM orders
GROUP BY status;

-- 8. Top Customers by Revenue
SELECT
    c.customer_id,
    c.name,
    c.email,
    c.country,
    COUNT(o.order_id) AS order_count,
    SUM(o.total_amount) AS total_revenue,
    AVG(o.total_amount) AS avg_order_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.email, c.country
ORDER BY total_revenue DESC
LIMIT 10;

-- 9. Inventory Analysis (Products with Low Stock)
SELECT
    product_id,
    name,
    category,
    stock_quantity,
    total_quantity_sold,
    CASE
        WHEN stock_quantity < 100 THEN 'Low Stock'
        WHEN stock_quantity < 500 THEN 'Medium Stock'
        ELSE 'High Stock'
    END AS stock_level
FROM products
ORDER BY stock_quantity ASC
LIMIT 20;

-- 10. Geographic Sales Analysis
SELECT
    c.country,
    COUNT(DISTINCT c.customer_id) AS customer_count,
    COUNT(o.order_id) AS order_count,
    SUM(o.total_amount) AS total_revenue,
    AVG(o.total_amount) AS avg_order_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.country
ORDER BY total_revenue DESC;
