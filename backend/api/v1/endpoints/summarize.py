from fastapi import APIRouter, UploadFile, File
from schemas.schemas import TextInput, SummaryResponse
from services.summarizer import summarize_text #summarize_uploaded_file

router = APIRouter()

@router.post("/", response_model=SummaryResponse)
async def summarize_text_route(input: TextInput):
    summary = summarize_text(input.text)
    return {"summary": summary}

"""
@router.post("/upload", response_model=SummaryResponse)
async def summarize_file_route(file: UploadFile = File(...)):
    summary = await summarize_uploaded_file(file)
    return {"summary": summary}
"""