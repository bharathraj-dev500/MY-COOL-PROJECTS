from fastapi import APIRouter
from app.services.ai_service import get_ai_response
from app.models.request_model import Query

router = APIRouter(
    prefix="/chat",
    tags=["Chatbot"]
)

@router.post("/ask")
async def ask_question(query: Query):
    response = get_ai_response(query.question)
    return {"answer": response}
