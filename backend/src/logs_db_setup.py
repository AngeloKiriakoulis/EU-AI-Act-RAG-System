import os
import psycopg2
from dotenv import load_dotenv

def setup_logs_database():
    load_dotenv()

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "logs_db"),  
        port=os.getenv("DB_PORT", 5433),
        dbname="postgres",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    
    conn.autocommit = True
    cur = conn.cursor()
    
    # Create logs database if it doesn't exist
    cur.execute("SELECT 1 FROM pg_database WHERE datname = 'logs'")
    exists = cur.fetchone()
    
    if not exists:
        cur.execute('CREATE DATABASE logs')
    
    # Close connection to default database
    cur.close()
    conn.close()
    
    # Connect to logs database
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "logs_db"),
        port=os.getenv("DB_PORT", 5433),
        dbname="logs",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    
    conn.autocommit = True
    cur = conn.cursor()
    
    # Create table for storing query logs
    cur.execute('''
        CREATE TABLE IF NOT EXISTS query_logs (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            top_chunks JSONB,
            distances FLOAT[]
        )
    ''')
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    setup_logs_database() 