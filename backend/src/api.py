from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import traceback

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
except Exception as e:
    print(f"Error initializing QA system: {e}")
    print(traceback.format_exc())
    qa_system = None  # Prevent FastAPI from restarting infinitely

class Question(BaseModel):
    text: str

# Before response was a raw dict. With Pydantic we can have structured, typed responses.
class ChunkMetadata(BaseModel):
    text: str
    metadata: dict
    distance: float

class AnswerResponse(BaseModel):
    answer: str
    chunks: list[ChunkMetadata]

@app.post("/api/ask")
async def ask_question(question: Question):
    if qa_system is None:
        raise HTTPException(status_code=500, detail="QA system failed to initialize.")
    try:
        # Get relevant chunks
        relevant_chunks = qa_system.get_relevant_chunks(question.text)
        
        # Generate answer
        answer = qa_system.generate_answer(question.text, relevant_chunks)

        qa_system.log_query(question.text,relevant_chunks=relevant_chunks,answer = answer)
        
        return AnswerResponse(answer=answer, chunks=relevant_chunks)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


# Basic endpoints to monitor deployment easily.
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/info")
def info():
    return {
        "model": "gemini-1.5-pro",
        "embedding_model": "voyage-2",
        "chunk_limit": 3
    }