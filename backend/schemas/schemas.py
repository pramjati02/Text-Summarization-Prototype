from pydantic import BaseModel

class TextInput(BaseModel):
    text: str
    
class SummaryResponse(BaseModel):
    summary: str