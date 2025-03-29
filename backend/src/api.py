from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
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

@app.post("/api/ask")
async def ask_question(question: Question):
    if qa_system is None:
        raise HTTPException(status_code=500, detail="QA system failed to initialize.")
    
    try:
        # Get relevant chunks
        relevant_chunks = qa_system.get_relevant_chunks(question.text)
        
        # Generate answer
        answer = qa_system.generate_answer(question.text, relevant_chunks)
        
        return {
            "answer": answer,
            "chunks": relevant_chunks
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))
