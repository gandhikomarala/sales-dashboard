# Data Processing Simulation Project

## Overview

This project simulates an end-to-end data pipeline for a hypothetical e-commerce platform using Python, SQL, and AWS concepts. It demonstrates data extraction, transformation, loading (ETL), data governance, and analytical querying capabilities.

## Features

- **Data Generation**: Synthetic e-commerce data generation (customers, products, orders)
- **ETL Pipeline**: Extract, Transform, Load process with data cleaning and aggregation
- **Data Governance**: Automated data quality checks and validation
- **SQL Analytics**: Comprehensive queries for business intelligence
- **AWS Simulation**: Local simulation of S3 storage concepts
- **Documentation**: Detailed data flow and optimization strategies

## Project Structure

```
├── data/
│   ├── raw/           # Raw CSV data files
│   └── processed/     # Transformed data and SQLite database
├── scripts/
│   ├── generate_data.py   # Data generation script
│   ├── etl.py            # ETL pipeline
│   └── governance.py     # Data quality validation
├── sql/
│   └── queries.sql       # Analytical SQL queries
├── docs/
│   └── data_flow.md      # Pipeline documentation
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Architecture

### Data Pipeline Flow

1. **Data Generation** → Raw CSV files in `data/raw/`
2. **ETL Process**:
   - Extract: Read raw data
   - Transform: Clean, aggregate, derive metrics
   - Load: Save to `data/processed/` (S3 simulation) and SQLite DB
3. **Data Governance**: Validate data integrity and relationships
4. **Analytics**: Query processed data using SQL

### AWS Concepts Demonstrated

- **S3**: Simulated through local file storage in `data/processed/`
- **ETL**: Implemented using Python with pandas
- **Data Lake**: Local directory structure mimicking cloud storage

## Installation

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Generate Sample Data**:
   ```bash
   python scripts/generate_data.py
   ```

2. **Run ETL Pipeline**:
   ```bash
   python scripts/etl.py
   ```

3. **Run Data Governance Checks**:
   ```bash
   python scripts/governance.py
   ```

4. **Execute SQL Queries**:
   Use SQLite to run queries from `sql/queries.sql` on `data/processed/ecommerce.db`

## Data Schema

### Customers
- customer_id (int)
- name (string)
- email (string)
- age (int)
- country (string)
- registration_date (datetime)
- age_group (derived)
- total_spent (derived)
- avg_order_value (derived)
- order_count (derived)
- last_order_date (derived)

### Products
- product_id (int)
- name (string)
- category (string)
- price (float)
- stock_quantity (int)
- total_quantity_sold (derived)
- total_revenue (derived)

### Orders
- order_id (int)
- customer_id (int)
- order_date (datetime)
- total_amount (float)
- status (string)

### Order Items
- order_id (int)
- product_id (int)
- quantity (int)
- unit_price (float)
- item_total (float)

## Key Features

### ETL Transformations
- Data cleaning and missing value handling
- Date parsing and formatting
- Customer segmentation by age groups
- Order aggregation metrics
- Product performance calculations

### Data Governance
- Null value detection
- Duplicate key validation
- Data type consistency checks
- Referential integrity validation
- Automated quality reporting

### Analytical Capabilities
- Sales and revenue analysis
- Customer lifetime value calculation
- Product performance metrics
- Geographic sales distribution
- Temporal trend analysis

## Optimization Strategies

- **Memory Efficiency**: Chunked data processing for large datasets
- **Indexing**: SQLite indexes on frequently queried columns
- **Caching**: In-memory aggregations where possible
- **Parallel Processing**: Potential for distributed ETL in cloud environments
- **Incremental Loading**: Framework for delta updates

## Academic Learning Outcomes

This project demonstrates:
- Python data manipulation with pandas
- SQL querying and database design
- ETL pipeline development
- Data quality assurance practices
- Cloud data storage concepts (AWS S3)
- Business intelligence through data analysis

## Future Enhancements

- Real-time data streaming simulation
- Machine learning model integration
- Dashboard visualization
- Multi-cloud deployment
- Automated testing suite
