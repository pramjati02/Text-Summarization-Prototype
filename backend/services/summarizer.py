from models.summarizer_models import model_bart, tokenizer_bart, model_t5, tokenizer_t5, model_pegasus, tokenizer_pegasus
import torch
import fitz # for pdf file upload and extraction
import re

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def preprocess_text(text: str) -> str:
    # lowercase text
    text = text.lower()
    
    # preserve contractions such as don't, can't etc.
    text = re.sub(r"(?!\b\w*'\w*\b)([^\w\s'])", r' \1 ', text)
    
    # Collapse multiple spaces 
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text 

def capitalize_sentences(text: str) -> str:
    # Split by sentence boundaries (.!?), keeping the punctuation
    sentences = re.split(r'([.!?])', text)
    
    # Reconstruct sentences with capitalization
    capitalized = []
    for i in range(0, len(sentences) - 1, 2):
        sentence = sentences[i].strip().capitalize()
        punctuation = sentences[i+1]
        capitalized.append(sentence + punctuation)
    
    # Handle possible trailing text
    if len(sentences) % 2 != 0:
        capitalized.append(sentences[-1].strip().capitalize())

    return ' '.join(capitalized)

# extract text from a given uploaded pdf file 
def extract_text_pdf(file_bytes: bytes) -> str:
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        return " ".join([page.get_text() for page in doc])

### TEXT SUMMARIZATION FOR BART ###

def summarize_text_bart(text:str) -> str:
    text = preprocess_text(text)
    inputs = tokenizer_bart(text, return_tensors="pt", truncation=True, max_length=1024).to(device)
    summary_ids = model_bart.generate(inputs["input_ids"], 
                                 max_length=256, 
                                 min_length=30,
                                 length_penalty=-2.0,
                                 num_beams = 4, 
                                 early_stopping=True,
                                 )
    return tokenizer_bart.decode(summary_ids[0], skip_special_tokens=True)


async def summarize_uploaded_file_bart(file) -> str:
    contents = await file.read()
    text = extract_text_pdf(contents)
    text_summary = summarize_text_bart(text)
    #print("Summary:", summary)
    summary = capitalize_sentences(text_summary)
    return summary
    
### TEXT SUMMARIZATION FOR T5 ###

def summarize_text_t5(text:str) -> str:
    text = preprocess_text(text)
    inputs = tokenizer_t5(text, return_tensors="pt", truncation=True, max_length=1024).to(device)
    summary_ids = model_t5.generate(inputs["input_ids"], 
                                 max_length=256, 
                                 min_length=30,
                                 length_penalty=-2.0,
                                 num_beams = 4, 
                                 early_stopping=True,
                                 )
    return tokenizer_t5.decode(summary_ids[0], skip_special_tokens=True)


async def summarize_uploaded_file_t5(file) -> str:
    contents = await file.read()
    text = extract_text_pdf(contents)
    text_summary = summarize_text_t5(text)
    #print("Summary:", summary)
    summary = capitalize_sentences(text_summary)
    return summary


### TEXT SUMMARIZATION FOR PEGASUS ###

def summarize_text_pegasus(text:str) -> str:
    text = preprocess_text(text)
    inputs = tokenizer_pegasus(text, return_tensors="pt", truncation=True, max_length=1024).to(device)
    summary_ids = model_pegasus.generate(inputs["input_ids"], 
                                 max_length=256, 
                                 min_length=30,
                                 length_penalty=-2.0,
                                 num_beams = 4, 
                                 early_stopping=True,
                                 )
    return tokenizer_pegasus.decode(summary_ids[0], skip_special_tokens=True)


async def summarize_uploaded_file_pegasus(file) -> str:
    contents = await file.read()
    text = extract_text_pdf(contents)
    text_summary = summarize_text_pegasus(text)
    #print("Summary:", summary)
    summary = capitalize_sentences(text_summary)
    return summary