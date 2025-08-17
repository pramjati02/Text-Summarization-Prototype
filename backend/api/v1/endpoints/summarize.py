from fastapi import APIRouter, UploadFile, File
from schemas.schemas import TextInput, SummaryResponse
from services.summarizer import summarize_text_bart, summarize_uploaded_file_bart, summarize_uploaded_file_t5, summarize_text_t5, summarize_uploaded_file_pegasus

router = APIRouter()

"""
@router.post("/summarize/", response_model=SummaryResponse)
async def summarize_text_route(input: TextInput):
    summary = summarize_text(input.text)
    return {"summary": summary}
"""

@router.post("/", response_model=SummaryResponse)
async def summarize_file_route_bart(file: UploadFile = File(...)):
    summary = await summarize_uploaded_file_bart(file)
    return {"summary": summary}

@router.post("/t5/", response_model=SummaryResponse)
async def summarize_file_route_t5(file: UploadFile = File(...)):
    summary = await summarize_uploaded_file_t5(file)
    return {"summary": summary}


@router.post("/pegasus/", response_model=SummaryResponse)
async def summarize_file_route_pegasus(file: UploadFile = File(...)):
    summary = await summarize_uploaded_file_pegasus(file)
    return {"summary": summary}
