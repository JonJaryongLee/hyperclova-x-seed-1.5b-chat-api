from fastapi import APIRouter
from app.models import prepare_inputs, generate_response
from app.schemas import ChatRequest

router = APIRouter(prefix="/v1/chat")

@router.post("/completions")
async def chat(req: ChatRequest):
    msgs = [m.model_dump() for m in req.messages]
    inputs = prepare_inputs(msgs)

    reply = generate_response(inputs)

    return {"reply": reply}