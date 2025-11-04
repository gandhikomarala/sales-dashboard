import pandas as pd
import logging
import sqlite3
from datetime import datetime

logger = logging.getLogger(__name__)

def validate_data_integrity(df, table_name):
    """Validate data integrity for a DataFrame."""
    issues = []

    # Check for null values in critical columns
    critical_columns = {
        'customers': ['customer_id', 'name', 'email'],
        'products': ['product_id', 'name', 'price'],
        'orders': ['order_id', 'customer_id', 'total_amount'],
        'order_items': ['order_id', 'product_id', 'quantity']
    }

    if table_name in critical_columns:
        for col in critical_columns[table_name]:
            if col in df.columns:
                null_count = df[col].isnull().sum()
                if null_count > 0:
                    issues.append(f"Column '{col}' has {null_count} null values")

    # Check for duplicate primary keys
    primary_keys = {
        'customers': 'customer_id',
        'products': 'product_id',
        'orders': 'order_id'
    }

    if table_name in primary_keys:
        pk_col = primary_keys[table_name]
        if pk_col in df.columns:
            duplicates = df[df.duplicated(subset=[pk_col], keep=False)]
            if not duplicates.empty:
                issues.append(f"Found {len(duplicates)} duplicate {pk_col} values")

    # Check for negative values in numeric columns
    numeric_columns = ['price', 'total_amount', 'quantity', 'item_total']
    for col in numeric_columns:
        if col in df.columns:
            negative_count = (df[col] < 0).sum()
            if negative_count > 0:
                issues.append(f"Column '{col}' has {negative_count} negative values")

    # Check for data type consistency
    if 'price' in df.columns:
        non_numeric_prices = pd.to_numeric(df['price'], errors='coerce').isnull().sum()
        if non_numeric_prices > 0:
            issues.append(f"Column 'price' has {non_numeric_prices} non-numeric values")

    return issues

def validate_relationships(conn):
    """Validate relationships between tables."""
    issues = []

    try:
        # Check if all order customer_ids exist in customers table
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM orders o
            LEFT JOIN customers c ON o.customer_id = c.customer_id
            WHERE c.customer_id IS NULL
        """)
        orphaned_orders = cursor.fetchone()[0]
        if orphaned_orders > 0:
            issues.append(f"Found {orphaned_orders} orders with non-existent customer_ids")

        # Check if all order_items product_ids exist in products table
        cursor.execute("""
            SELECT COUNT(*) FROM order_items oi
            LEFT JOIN products p ON oi.product_id = p.product_id
            WHERE p.product_id IS NULL
        """)
        orphaned_items = cursor.fetchone()[0]
        if orphaned_items > 0:
            issues.append(f"Found {orphaned_items} order items with non-existent product_ids")

        # Check if all order_items order_ids exist in orders table
        cursor.execute("""
            SELECT COUNT(*) FROM order_items oi
            LEFT JOIN orders o ON oi.order_id = o.order_id
            WHERE o.order_id IS NULL
        """)
        orphaned_order_items = cursor.fetchone()[0]
        if orphaned_order_items > 0:
            issues.append(f"Found {orphaned_order_items} order items with non-existent order_ids")

    except Exception as e:
        issues.append(f"Error validating relationships: {e}")

    return issues

def generate_data_quality_report():
    """Generate a comprehensive data quality report."""
    report = {
        'timestamp': datetime.now().isoformat(),
        'data_integrity_issues': {},
        'relationship_issues': [],
        'summary': {}
    }

    try:
        # Load data from SQLite
        conn = sqlite3.connect('data/processed/ecommerce.db')

        tables = ['customers', 'products', 'orders', 'order_items']
        total_records = 0

        for table in tables:
            df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
            total_records += len(df)

            # Validate data integrity
            issues = validate_data_integrity(df, table)
            if issues:
                report['data_integrity_issues'][table] = issues

        # Validate relationships
        report['relationship_issues'] = validate_relationships(conn)

        # Summary
        report['summary'] = {
            'total_records': total_records,
            'tables_processed': len(tables),
            'data_integrity_issues_count': sum(len(issues) for issues in report['data_integrity_issues'].values()),
            'relationship_issues_count': len(report['relationship_issues'])
        }

        conn.close()

    except Exception as e:
        logger.error(f"Error generating data quality report: {e}")
        report['error'] = str(e)

    return report

def log_data_quality_report(report):
    """Log the data quality report."""
    logger.info("=== Data Quality Report ===")
    logger.info(f"Timestamp: {report['timestamp']}")
    logger.info(f"Total Records: {report['summary'].get('total_records', 'N/A')}")
    logger.info(f"Tables Processed: {report['summary'].get('tables_processed', 'N/A')}")

    if report['data_integrity_issues']:
        logger.warning("Data Integrity Issues Found:")
        for table, issues in report['data_integrity_issues'].items():
            logger.warning(f"  {table}:")
            for issue in issues:
                logger.warning(f"    - {issue}")
    else:
        logger.info("No data integrity issues found.")

    if report['relationship_issues']:
        logger.warning("Relationship Issues Found:")
        for issue in report['relationship_issues']:
            logger.warning(f"  - {issue}")
    else:
        logger.info("No relationship issues found.")

    if 'error' in report:
        logger.error(f"Report generation error: {report['error']}")

def enforce_data_governance():
    """Main function to enforce data governance checks."""
    logger.info("Starting data governance checks...")

    report = generate_data_quality_report()
    log_data_quality_report(report)

    # Raise exception if critical issues found
    critical_issues = report['summary'].get('data_integrity_issues_count', 0) + report['summary'].get('relationship_issues_count', 0)
    if critical_issues > 0:
        logger.warning(f"Found {critical_issues} data quality issues. Pipeline may need attention.")
    else:
        logger.info("All data governance checks passed.")

    return report

if __name__ == "__main__":
    enforce_data_governance()
