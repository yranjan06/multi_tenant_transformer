# Multi-Tenant Transformation Engine

A lightweight Python-based transformation engine for multi-tenant SaaS applications. Each tenant gets isolated data storage while sharing transformation logic through templated SQL.

## What This Does

Modern SaaS applications need to serve multiple customers (tenants) while keeping their data completely separate. This project demonstrates how to:

- Keep each tenant's data in isolated databases
- Share transformation logic across all tenants  
- Configure tenant-specific behavior without code changes
- Process data transformations at scale

## Architecture

**Schema-per-tenant model**: Each tenant gets their own SQLite database for complete data isolation.

**Shared transformation engine**: All tenants use the same SQL templates, but with different variables.

**Configuration-driven**: Add new tenants or modify transformations by editing JSON config files.

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Basic understanding of SQL and CSV files

### Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install jinja2 
   ```

### Project Structure

```
multi_tenant_transformer/
├── config/
│   └── tenants.json              # Tenant configuration
├── tenants_data/
│   ├── tenant_alpha.csv          # Sample data for tenant A
│   ├── tenant_beta.csv           # Sample data for tenant B
│   ├── tenant_alpha.db           # Generated database
│   └── tenant_beta.db            # Generated database
├── tenant_manager/
│   └── manager.py                # Database initialization
├── transform_engine/
│   └── runner.py                 # Transformation execution
└── templates/
    └── transformation.sql.j2     # SQL template
```

### Running the System

**Step 1: Install requirements.txt**

**Step 2: Run transformations**
```bash
python transform_engine/runner.py
```

That's it. Each tenant's data will be transformed according to their specific configuration.

## How It Works

### 1. Configuration

Define your tenants in `config/tenants.json`:

```json
{
  "tenants": [
    {
      "id": "tenant_alpha",
      "name": "Alpha Corp",
      "database": "tenants_data/tenant_alpha.db",
      "source_csv": "tenants_data/tenant_alpha.csv",
      "table_name": "users",
      "transformations": {
        "transformation": "UPPER(name)",
        "output_column": "name_upper"
      }
    }
  ]
}
```

### 2. SQL Templates

Write reusable SQL in `templates/transformation.sql.j2`:

```sql
SELECT 
    id,
    name,
    email,
    {{ transformation }} AS {{ output_column }}
FROM {{ table_name }};
```

### 3. Data Processing

The engine reads your configuration, applies the SQL template to each tenant's data, and creates transformed tables.

## Example Use Case

**Tenant Alpha** needs customer names in uppercase:
- Input: "Ranjan Yadav"
- Transformation: `UPPER(name)`
- Output: "RANJAN YADAV"

**Tenant Beta** needs email addresses in lowercase:
- Input: "USER@COMPANY.COM"  
- Transformation: `LOWER(email)`
- Output: "user@company.com"

Both tenants use the same SQL template, but with different transformation variables.

## Adding New Tenants

1. Create a CSV file with your tenant's data
2. Add tenant configuration to `tenants.json`
3. Run the initialization and transformation scripts

No code changes required.

## Configuration Options

Each tenant can specify:

- **Database location**: Where to store their data
- **Source CSV**: Input data file
- **Table name**: What to call the table in their database
- **Transformations**: SQL expressions and column names

## Requirements

- Python 3.8+
- jinja2 (for SQL templating)
- pandas (for CSV processing)
- sqlite3 (built into Python)

## Use Cases

This pattern works well for:

- SaaS applications with customer-specific data processing
- ETL pipelines that need tenant isolation
- Reporting systems with customizable transformations
- Data warehouses serving multiple clients

## Inspiration

Built using architectural patterns from:

- "Multi-Tenant SaaS Architectures" (ResearchGate, 2024)  
- Cerbos multi-tenancy best practices

## What's Next

Some ideas for extending this project:

- Web interface for managing tenants
- Export results to different formats
- Parallel processing for better performance
- Data validation rules per tenant
- Integration with cloud databases

## License

MIT License - use this code however you want.

## Questions?

This is a learning project demonstrating multi-tenant architecture patterns. The code is intentionally simple to help you understand the concepts.

For production use, you'd want to add authentication, error handling, monitoring, and use a more robust database than SQLite.
