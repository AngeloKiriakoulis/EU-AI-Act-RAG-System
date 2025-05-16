"""Python version 3.12"""

import os

import psycopg2
from dotenv import load_dotenv


def setup_database():
    """
    Initialize Chunks Database
    """
    load_dotenv()

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname="postgres",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    conn.autocommit = True
    cur = conn.cursor()

    # Create database if it doesn't exist
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{os.getenv('DB_NAME')}'")
    exists = cur.fetchone()

    if not exists:
        cur.execute(f'CREATE DATABASE {os.getenv("DB_NAME")}')

    # Close connection to default database
    cur.close()
    conn.close()

    # Connect to our new database
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    conn.autocommit = True
    cur = conn.cursor()

    # Enable pgvector extension
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # Create table for storing chunks and embeddings
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS document_chunks (
            id SERIAL PRIMARY KEY,
            chunk_text TEXT NOT NULL,
            embedding vector(1024),
            metadata JSONB
        )
    """
    )

    cur.close()
    conn.close()


if __name__ == "__main__":
    setup_database()
