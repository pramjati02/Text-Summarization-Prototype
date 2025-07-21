from fastapi import APIRouter, UploadFile, File
from schemas.schemas import TextInput, SummaryResponse
from services.summarizer import summarize_text

router = APIRouter()

@router.post("/", response_model = SummaryResponse)
async def summarize_text_route(input: TextInput):
    summary = summarize_text(input.text)
    return {"summary": summary}