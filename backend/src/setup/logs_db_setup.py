import os
import psycopg2
from dotenv import load_dotenv

def setup_logs_database():
    load_dotenv()
    print("Connecting to", os.getenv("LOGS_HOST"), "on port", os.getenv("LOGS_DB_PORT"))
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=os.getenv("LOGS_HOST", "logs-db"),  
        port=int(os.getenv("LOGS_DB_PORT", 5432)),
        dbname='postgres',
        user=os.getenv("LOGS_USER"),
        password=os.getenv("LOGS_PASSWORD")
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
        host=os.getenv("LOGS_HOST", "logs-db"),
        port=int(os.getenv("LOGS_DB_PORT", 5432)),
        dbname=os.getenv("LOGS_DB", "logs"),
        user=os.getenv("LOGS_USER"),
        password=os.getenv("LOGS_PASSWORD")
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