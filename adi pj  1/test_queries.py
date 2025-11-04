import sqlite3

def run_queries():
    # Connect to the database
    conn = sqlite3.connect('data/processed/ecommerce.db')
    cursor = conn.cursor()

    # Read the SQL queries from the file
    with open('sql/queries.sql', 'r') as f:
        queries = f.read()

    # Split queries by semicolon and execute each one
    query_list = queries.split(';')
    for i, query in enumerate(query_list):
        query = query.strip()
        if query:
            print(f"Executing Query {i+1}: {query[:50]}...")
            try:
                cursor.execute(query)
                results = cursor.fetchall()
                if results:
                    print("Results (first 5 rows):")
                    for row in results[:5]:
                        print(row)
                else:
                    print("No results")
            except Exception as e:
                print(f"Error executing query: {e}")
            print("---")

    # Close the connection
    conn.close()

if __name__ == "__main__":
    run_queries()
