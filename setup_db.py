#!/usr/bin/env python
"""Setup the database by creating themis_dev if it doesn't exist."""

import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    """Create the database if it doesn't exist."""
    # Get connection string
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ DATABASE_URL not set in .env")
        return False

    # Extract credentials and database name
    # Format: postgresql://user:password@host:port/dbname
    try:
        parts = db_url.split("://")[1]
        credentials, host_db = parts.split("@")
        username, password = credentials.split(":")
        host_port, dbname = host_db.split("/", 1)
        if ":" in host_port:
            host, port = host_port.split(":")
            port = int(port)
        else:
            host = host_port
            port = 5432
    except Exception as e:
        print(f"❌ Failed to parse DATABASE_URL: {e}")
        return False

    # Connect to postgres (default) database to create our database
    try:
        conn = psycopg2.connect(
            user=username,
            password=password,
            host=host,
            port=port,
            database="postgres",
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Check if database exists
        cur.execute(
            sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"),
            [dbname]
        )
        exists = cur.fetchone()

        if exists:
            print(f"✓ Database '{dbname}' already exists")
        else:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(dbname)
            ))
            print(f"✓ Created database '{dbname}'")

        cur.close()
        conn.close()
        return True

    except Exception as e:
        print(f"❌ Failed to create database: {e}")
        return False


if __name__ == "__main__":
    if create_database():
        print("\n✅ Database setup complete!")
    else:
        print("\n❌ Database setup failed!")
        exit(1)
