#!/bin/bash
set -e

echo "🔍 Waiting for PostgreSQL to be ready..."

# Replace with your DB host and port
until pg_isready -h db -p 5432; do
  echo "⏳ Waiting for db to accept connections..."
  sleep 1
done

echo "✅ PostgreSQL is up!"

echo "🔍 Checking if databases need to be initialized..."

# Use a marker file to avoid re-running the setup
if [ ! -f /src/.db_initialized ]; then
  echo "⚙️ Initializing databases..."

  python /src/setup/db_setup.py
  python /src/setup/process_documents.py
  python /src/setup/logs_db_setup.py

  touch /src/.db_initialized
  echo "✅ Initialization complete."
else
  echo "🚀 Databases already initialized. Skipping setup."
fi

# Start the actual app
exec uvicorn api:app --host 0.0.0.0 --port 8000
