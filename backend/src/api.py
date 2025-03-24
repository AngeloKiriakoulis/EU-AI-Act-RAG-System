from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from .app import EUAIActQA
import traceback

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the QA system
qa_system = EUAIActQA()

class Question(BaseModel):
    text: str

@app.post("/api/ask")
async def ask_question(question: Question):
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