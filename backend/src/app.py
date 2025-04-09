import json
import os
import psycopg2
from dotenv import load_dotenv
from voyageai import Client
import google.generativeai as genai
from typing import List, Dict
from datetime import datetime
import traceback

class EUAIActQA:
    def __init__(self):
        load_dotenv()

        # Load environment variables
        self.voyage_client = Client(api_key=os.getenv('VOYAGE_API_KEY'))
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model = genai.GenerativeModel('gemini-1.5-pro')

    def get_db_connection(self):
        """Connect to main DB."""
        return psycopg2.connect(
            host='db',
            port=os.getenv('DB_PORT'),
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )

    def get_logs_db_connection(self):
        """Connect to logs DB."""
        return psycopg2.connect(
            host=os.getenv('LOGS_HOST'),
            port=os.getenv('LOGS_DB_PORT'),  # defaults to 5432 internally
            dbname=os.getenv('LOGS_DB'),
            user=os.getenv('LOGS_USER'),
            password=os.getenv('LOGS_PASSWORD')
        )

    def log_query(self, query: str, relevant_chunks: List[Dict], answer: str):
        """Insert query log into logs DB."""
        try:
            print("📝 Logging query to DB...")
            print("LOGS DB HOST:", os.getenv('LOGS_HOST'))
            print("LOGS DB PORT:", os.getenv('LOGS_DB_PORT'))
            conn = self.get_logs_db_connection()
            cur = conn.cursor()

            # Ensure table exists
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

            # ✅ Proper JSON serialization of chunks
            top_chunks_json = json.dumps(relevant_chunks)

            # ✅ Prepare distances as an array
            distances = [chunk['distance'] for chunk in relevant_chunks]

            # Insert record
            cur.execute(
                'INSERT INTO query_logs (question, answer, top_chunks, distances) VALUES (%s, %s, %s, %s)',
                (query, answer, top_chunks_json, distances)
            )

            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print("⚠️ Failed to log query:", e)
            print(traceback.format_exc())

    def get_relevant_chunks(self, query: str, k: int = 3) -> List[Dict]:
        """Retrieve the most relevant chunks for a given query."""
        query_embedding = self.voyage_client.embed([query], model="voyage-2").embeddings[0]
        
        conn = self.get_db_connection()
        cur = conn.cursor()

        cur.execute('''
            SELECT chunk_text, metadata, embedding <-> %s::vector as distance
            FROM document_chunks
            ORDER BY distance
            LIMIT %s
        ''', (query_embedding, k))

        results = [{
            'text': row[0],
            'metadata': row[1],
            'distance': row[2]
        } for row in cur.fetchall()]

        cur.close()
        conn.close()
        return results

    def generate_answer(self, query: str, relevant_chunks: List[Dict]) -> str:
        context = "\n\n".join([chunk['text'] for chunk in relevant_chunks])
        prompt = f"""Based on the following context from the EU AI Act, please answer the question.
        If the answer cannot be found in the context, say so.

        Context:
        {context}

        Question: {query}

        Answer:"""

        response = self.model.generate_content(prompt)
        return response.text

if __name__ == "__main__":
    qa = EUAIActQA()
    chunks = [
        {'text': 'Example text 1', 'metadata': {}, 'distance': 0.1},
        {'text': 'Example text 2', 'metadata': {}, 'distance': 0.2},
        {'text': 'Example text 3', 'metadata': {}, 'distance': 0.3},
    ]
    qa.log_query("What is the AI Act?", chunks, "It regulates AI use in the EU.")