# EU AI Act RAG System

A lightweight Retrieval-Augmented Generation (RAG) system designed to answer user questions about the European Union AI Act. This project uses FastAPI for the backend API, Voyage AI for embeddings, Google Gemini 1.5 Pro for answer generation, and PostgreSQL for both chunk storage and query logging.

---

## 🚀 Project Structure & Services

This system is containerized using Docker Compose and includes:

### 1. **FastAPI App**
- Serves as the main API to handle user questions.
- Retrieves relevant document chunks based on query embeddings.
- Generates answers using Google Gemini.
- Logs all user queries and the retrieved chunks into a separate logging database.

### 2. **Main PostgreSQL DB**
- Stores embedded chunks of the EU AI Act and their metadata.
- Used to retrieve the most relevant content for a user's query.

### 3. **Logs PostgreSQL DB**
- Stores logs of each user query, including:
  - The question
  - The generated answer
  - The top relevant chunks (as JSON)
  - The distances (similarity scores)

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **FastAPI**
- **psycopg2**
- **Voyage AI** (Embeddings)
- **Google Generative AI (Gemini)**
- **PostgreSQL**
- **Docker & Docker Compose**
- **PgAdmin4** (for DB browsing)

---

## 📦 Getting Started

### 1. Clone the Repo
```bash
git clone https://github.com/your-username/eu-ai-act-rag.git
cd eu-ai-act-rag
```

### 2. Environment Variables
Create a `.env` file:
```env
# Main DB
DB_NAME=eu_act
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_PORT=5432

# Logs DB
LOGS_DB=eu_logs
LOGS_USER=postgres
LOGS_PASSWORD=yourpassword
LOGS_DB_PORT=5432
LOGS_HOST=logs_db

# APIs
VOYAGE_API_KEY=your_voyage_api_key
GOOGLE_API_KEY=your_google_api_key
```

### 3. Start the System
```bash
docker compose up --build
```

### 4. Access PgAdmin
PgAdmin is available at `http://localhost:5050`
- Default credentials: `pgadmin4@admin.com / admin`
- Add connections to `db` and `logs_db` containers

---

## 📡 API Endpoints

### POST `/api/ask`
Request Body:
```json
{
  "text": "What is the AI Act?"
}
```
Response:
```json
{
  "answer": "The AI Act regulates the use of AI in the EU...",
  "chunks": [
    {
      "text": "Relevant chunk text...",
      "metadata": {...},
      "distance": 0.14
    },
    ...
  ]
}
```

### GET `/health`
Returns: `{ "status": "ok" }`

### GET `/info`
Returns basic model info:
```json
{
  "model": "gemini-1.5-pro",
  "embedding_model": "voyage-2",
  "chunk_limit": 3
}
```

---

## 📋 Logging Schema (Logs DB)

```sql
CREATE TABLE IF NOT EXISTS query_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    top_chunks JSONB,
    distances FLOAT[]
);
```

---

## 🙌 Credits
Created by Aggelos as a robust, developer-friendly system to experiment with modern GenAI tools applied to real EU policy documents.

---