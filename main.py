
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from crawler.rag_pipeline import ask_question


# --------------------------------
# 1. CREATE FASTAPI APPLICATION
# --------------------------------

app = FastAPI(
    title="Skill Learning Academy AI Chatbot",
    description="Website-wide RAG chatbot API",
    version="1.0.0"
)


# --------------------------------
# 2. CORS CONFIGURATION
# --------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this to your website in production
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------
# 3. REQUEST MODEL
# --------------------------------

class ChatRequest(BaseModel):
    question: str


# --------------------------------
# 4. HEALTH CHECK
# --------------------------------

@app.get("/")
def home():
    return {
        "message": "Skill Learning Academy AI Chatbot API is running!"
    }


# --------------------------------
# 5. CHAT ENDPOINT
# --------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:

        answer = ask_question(question)

        return {
            "question": question,
            "answer": answer
        }

    except Exception as error:

        print("Chatbot error:", error)

        raise HTTPException(
            status_code=500,
            detail="Something went wrong while generating the answer."
        )
