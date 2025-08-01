# SQLite doesn’t support multiple schemas per DB like PostgreSQL,
# so we isolate tenants using one database file per tenant.

import sqlite3
import json
import os
import csv
from jinja2 import Template

CONFIG_PATH = "config/tenants.json"
TEMPLATE_PATH = "templates/transformation.sql.j2"

def initialize_tenant_db(tenant_config):
    """Create and populate SQLite database for a tenant"""
    db_path = tenant_config['db_path']
    csv_path = tenant_config['input_csv']
    table = tenant_config['vars']['table']

    # Skip if database already exists
    if os.path.exists(db_path):
        return

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

    print(f"Database initialized: {tenant_config['id']} -> {table} ({len(rows)} records)")

def load_tenant_config():
    """Load tenant configurations from JSON"""
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)['tenants']

def load_sql_template():
    """Load Jinja2 SQL template"""
    with open(TEMPLATE_PATH, 'r') as f:
        return Template(f.read())

def execute_transformation(tenant, template):
    """Run transformation for a specific tenant"""
    # Auto-initialize database if needed
    initialize_tenant_db(tenant)
    
    # Render SQL with tenant-specific variables
    sql_query = template.render(**tenant['vars'])
    
    # Execute against tenant database
    conn = sqlite3.connect(tenant['db_path'])
    cursor = conn.cursor()
    
    print(f"\nProcessing: {tenant['id']}")
    print(f"SQL: {sql_query.strip()}")
    
    results = cursor.execute(sql_query).fetchall()
    
    print("Results:")
    for row in results:
        print(f"  {row}")
    
    conn.close()

def main():
    """Main execution function"""
    tenants = load_tenant_config()
    template = load_sql_template()
    
    print("Multi-Tenant Transformation Engine Starting...")
    
    for tenant in tenants:
        execute_transformation(tenant, template)
    
    print("\nTransformation complete!")

if __name__ == '__main__':
    main()
