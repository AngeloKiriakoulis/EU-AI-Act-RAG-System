import os
import psycopg2
from dotenv import load_dotenv
from voyageai import Client
import google.generativeai as genai
from typing import List, Dict

class EUAIActQA:
    def __init__(self):
        load_dotenv()
        self.voyage_client = Client(api_key=os.getenv('VOYAGE_API_KEY'))
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        
    def get_db_connection(self):
        load_dotenv()
        return psycopg2.connect(
            # host=os.getenv('DB_HOST'),
            host='db',
            port=os.getenv('DB_PORT'),
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
    
    def get_relevant_chunks(self, query: str, k: int = 3) -> List[Dict]:
        """Retrieve the most relevant chunks for a given query."""
        # Create embedding for the query
        query_embedding = self.voyage_client.embed([query], model="voyage-2").embeddings[0]
        
        # Connect to database and perform similarity search
        conn = self.get_db_connection()
        cur = conn.cursor()
        
        cur.execute('''
            SELECT chunk_text, metadata, embedding <-> %s::vector as distance
            FROM document_chunks
            ORDER BY distance
            LIMIT %s
        ''', (query_embedding, k))
        
        results = []
        for row in cur.fetchall():
            results.append({
                'text': row[0],
                'metadata': row[1],
                'distance': row[2]
            })
        
        cur.close()
        conn.close()
        
        return results
    
    def generate_answer(self, query: str, relevant_chunks: List[Dict]) -> str:
        """Generate an answer using the Gemini model."""
        # Prepare context from relevant chunks
        context = "\n\n".join([chunk['text'] for chunk in relevant_chunks])
        
        # Create prompt for the model
        prompt = f"""Based on the following context from the EU AI Act, please answer the question.
        If the answer cannot be found in the context, say so.

        Context:
        {context}

        Question: {query}

        Answer:"""
        
        # Generate response
        response = self.model.generate_content(prompt)
        return response.text

def main():
    try:
        qa_system = EUAIActQA()  # If this crashes, we handle the error
    except Exception as e:
        import traceback
        print(f"Error initializing QA system: {e}")
        print(traceback.format_exc())
        qa_system = None  # Prevent crash loops    
    print("Welcome to the EU AI Act Q&A System!")
    print("Type 'quit' to exit.")
    
    while True:
        query = input("\nYour question: ").strip()
        if query.lower() == 'quit':
            break
            
        if not query:
            continue
            
        print("\nSearching for relevant information...")
        relevant_chunks = qa_system.get_relevant_chunks(query)
        print(relevant_chunks)
        print("\nGenerating answer...")
        answer = qa_system.generate_answer(query, relevant_chunks)
        
        print("\nAnswer:")
        print(answer)

# if __name__ == "__main__":
#     main() 