from fastapi import FastAPI
from pydantic import BaseModel
from engine import generate_reply
app = FastAPI(title="SAHELI Chatbot API")

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    return generate_reply(req.message)
