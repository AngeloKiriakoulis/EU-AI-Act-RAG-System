"""Python version 3.12"""

import traceback

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app import EUAIActQA

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow frontend to access API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Try initializing the QA system
try:
    qa_system = EUAIActQA()
except (KeyError, ValueError, TypeError, ConnectionError, RuntimeError) as e:
    print(f"Error initializing QA system: {e}")
    print(traceback.format_exc())


class Question(BaseModel):
    """
    Schema for the input question sent by the user.

    Attributes:
        text (str): The natural language question to be answered.
    """

    text: str


# Before response was a raw dict. With Pydantic we can have structured,
# typed responses.
class ChunkMetadata(BaseModel):
    """
    Schema for metadata of each relevant document chunk.

    Attributes:
        text (str): Text content of the chunk.
        metadata (dict): Associated metadata (e.g. source, section).
        distance (float): Vector similarity distance from the query.
    """

    text: str
    metadata: dict
    distance: float


class AnswerResponse(BaseModel):
    """
    Schema for the complete answer response returned by the QA system.

    Attributes:
        answer (str): Generated answer to the input question.
        chunks (list[ChunkMetadata]): Relevant document chunks
        used for the answer.
    """

    answer: str
    chunks: list[ChunkMetadata]


@app.post("/api/ask")
async def ask_question(question: Question):
    """
    Endpoint to submit a question and receive an AI-generated answer.

    Args:
        question (Question): A Pydantic model containing the question text.

    Returns:
        AnswerResponse: The generated answer and relevant document chunks.

    Raises:
        HTTPException: If the QA system fails or encounters a runtime error.
    """
    if qa_system is None:
        raise HTTPException(status_code=500, detail="QA system failed to initialize.")
    try:
        # Get relevant chunks
        relevant_chunks = qa_system.get_relevant_chunks(question.text)

        # Generate answer
        answer = qa_system.generate_answer(question.text, relevant_chunks)

        qa_system.log_query(
            question.text, relevant_chunks=relevant_chunks, answer=answer
        )

        return AnswerResponse(answer=answer, chunks=relevant_chunks)

    except HTTPException as e:
        print(f"Error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e)) from e


# Basic endpoints to monitor deployment easily.
@app.get("/health")
def health_check():
    """
    Retrieve the status of the API app.

    Returns:
        dict: A dictionary containing the status of the app.
    """
    return {"status": "ok"}


@app.get("/info")
def info():
    """Returns information about the tools we use, currently static

    Returns:
        type(dict): key, value pairs for all the tools/parameters we use.
    """
    return {"model": "gemini-1.5-pro", "embedding_model": "voyage-2", "chunk_limit": 3}
