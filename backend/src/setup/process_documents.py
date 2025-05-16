"""Python version 3.12"""

import json
import os
from typing import Dict, List

import psycopg2
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter  # type: ignore
from voyageai import Client  # type: ignore


def load_documents(directory: str) -> List[str]:
    """Load all text files from the specified directory."""
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as f:
                documents.append(f.read())
    return documents


def split_documents(
    documents: List[str], chunk_size: int = 1000, chunk_overlap: int = 200
) -> List[str]:
    """Split documents into chunks using LangChain's text splitter."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""],
    )

    chunks = []
    for doc in documents:
        chunks.extend(text_splitter.split_text(doc))
    return chunks


def create_embeddings(chunks: List[str], voyage_client: Client) -> List[List[float]]:
    """Create embeddings for text chunks using Voyage AI."""
    embeddings = []
    for chunk in chunks:
        embedding = voyage_client.embed([chunk], model="voyage-2")
        embeddings.append(embedding.embeddings[0])
    return embeddings


def store_chunks_and_embeddings(
    chunks: List[str], embeddings: List[List[float]], metadata: List[Dict]
):
    """Store chunks and their embeddings in the PostgreSQL database."""
    load_dotenv()

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    cur = conn.cursor()

    for chunk, embedding, meta in zip(chunks, embeddings, metadata):
        cur.execute(
            "INSERT INTO document_chunks (chunk_text, embedding, metadata) VALUES (%s, %s, %s)",
            (chunk, embedding, json.dumps(meta)),
        )

    conn.commit()
    cur.close()
    conn.close()


def main():
    """
    Main script to fill up the chunks database.
    """
    load_dotenv()
    # Initialize Voyage AI client
    voyage_client = Client(api_key=os.getenv("VOYAGE_API_KEY"))

    # Load and process documents
    documents = load_documents("articles")
    chunks = split_documents(documents)

    # Create embeddings
    embeddings = create_embeddings(chunks, voyage_client)

    # Create metadata for each chunk
    metadata = [{"source": "EU AI Act", "chunk_index": i} for i in range(len(chunks))]

    # Store in database
    store_chunks_and_embeddings(chunks, embeddings, metadata)


if __name__ == "__main__":
    main()
