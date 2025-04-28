from fastapi import FastAPI
from app.routers import chat

app = FastAPI(
    title="Chatbot API",
    description="A FastAPI + LangChain based Chatbot",
    version="1.0.0"
)

app.include_router(chat.router)