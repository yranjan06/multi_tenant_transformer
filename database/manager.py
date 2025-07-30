import sqlite3
import csv
import os

def initialize_tenant_db(tenant_config):
    """Create and populate SQLite database for a tenant"""
    db_path = tenant_config['db_path']
    csv_path = tenant_config['input_csv']
    table = tenant_config['vars']['table']

    # Ensure directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Read CSV data
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    # Create table schema dynamically
    columns = ', '.join([f'{col} TEXT' for col in header])
    placeholders = ', '.join(['?' for _ in header])

    # Initialize database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(f'DROP TABLE IF EXISTS {table}')
    cur.execute(f'CREATE TABLE {table} ({columns})')
    cur.executemany(f'INSERT INTO {table} VALUES ({placeholders})', rows)
    conn.commit()
    conn.close()

    print(f"Database ready: {tenant_config['id']} -> {table} ({len(rows)} records)")