from models.summarizer_models import model, tokenizer
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def summarize_text(text:str) -> str:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=1024).to(device)
    summary_ids = model.generate(inputs["input_ids"], 
                                 max_length=256, 
                                 min_length=30,
                                 length_penalty=-2.0,
                                 num_beams = 4, 
                                 early_stopping=True,
                                 )
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

"""

async def summarize_uploaded_file(file) -> str:
    contents = await file.read()
    return summarize_text(contents.decode("utf-8"))
    
"""