"""
One-time data migration: adds a `tenant_id` column to existing MySQL tables
and populates it for all rows, enabling Django's TenantAwareManager to work
with pre-existing data.

Run on the Contabo server:
    python api/migrate_tenant_data.py

This script:
1. Adds a `tenant_id` column to tables that don't have it
2. Sets tenant_id for all existing rows to a specified tenant UUID
3. For the `users` table, also adds a `tenant_id` column if missing

Usage:
    python migrate_tenant_data.py --host 213.199.41.219 --user longhorn --password 3577 --database longhorn --tenant-id <uuid>
"""
import argparse
import uuid
import pymysql
from pymysql.cursors import DictCursor


def get_tables_without_tenant(cursor, database):
    """Get list of tables missing a tenant_id column."""
    query = """
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = %s
          AND COLUMN_NAME = 'tenant_id'
    """
    cursor.execute(query, (database,))
    tables_with_tenant = {row['TABLE_NAME'] for row in cursor.fetchall()}

    query_all = """
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = %s
          AND TABLE_TYPE = 'BASE TABLE'
          AND TABLE_NAME != 'tenants'
    """
    cursor.execute(query_all, (database,))
    all_tables = {row['TABLE_NAME'] for row in cursor.fetchall()}

    return all_tables - tables_with_tenant


def add_tenant_column(cursor, table_name):
    """Add tenant_id column to a table."""
    # Use VARCHAR(36) to match UUID format
    alter_query = f"ALTER TABLE `{table_name}` ADD COLUMN `tenant_id` VARCHAR(36) NULL"
    cursor.execute(alter_query)
    print(f"  Added tenant_id to {table_name}")


def populate_tenant_id(cursor, table_name, tenant_id):
    """Set tenant_id for all rows in a table."""
    update_query = f"UPDATE `{table_name}` SET `tenant_id` = %s WHERE `tenant_id` IS NULL"
    cursor.execute(update_query, (tenant_id,))
    affected = cursor.rowcount
    print(f"  Populated tenant_id for {affected} rows in {table_name}")


def main():
    parser = argparse.ArgumentParser(description='Migrate tenant data for Django')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=3306)
    parser.add_argument('--user', default='longhorn')
    parser.add_argument('--password', default='')
    parser.add_argument('--database', default='longhorn')
    parser.add_argument('--tenant-id', required=True, help='UUID of the tenant to assign')
    args = parser.parse_args()

    conn = pymysql.connect(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        database=args.database,
        charset='utf8mb4',
        cursorclass=DictCursor,
    )

    try:
        with conn.cursor() as cursor:
            print("Checking tables for tenant_id column...")
            tables_without = get_tables_without_tenant(cursor, args.database)

            if not tables_without:
                print("All tables already have tenant_id. Skipping column addition.")
            else:
                print(f"Found {len(tables_without)} tables missing tenant_id:")
                for table in sorted(tables_without):
                    print(f"  - {table}")

                print("\nAdding tenant_id columns...")
                for table in sorted(tables_without):
                    try:
                        add_tenant_column(cursor, table)
                    except Exception as e:
                        print(f"  ERROR on {table}: {e}")

            conn.commit()

            print(f"\nPopulating tenant_id = {args.tenant_id} for all tables...")

            cursor.execute(f"""
                SELECT TABLE_NAME
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_SCHEMA = %s
                  AND TABLE_TYPE = 'BASE TABLE'
                  AND TABLE_NAME != 'tenants'
            """, (args.database,))
            all_tables = [row['TABLE_NAME'] for row in cursor.fetchall()]

            for table in all_tables:
                try:
                    populate_tenant_id(cursor, table, args.tenant_id)
                except Exception as e:
                    print(f"  ERROR on {table}: {e}")

            conn.commit()
            print("\nMigration complete!")

    finally:
        conn.close()


if __name__ == '__main__':
    main()
