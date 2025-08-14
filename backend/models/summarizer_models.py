from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Check if torch is using cuda 
print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("CUDA device name:", torch.cuda.get_device_name(0))

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer_bart = AutoTokenizer.from_pretrained("pramjati02/bart-base-trained")
model_bart = AutoModelForSeq2SeqLM.from_pretrained("pramjati02/Bart-Base-Trained").to(device)

tokenizer_t5 = AutoTokenizer.from_pretrained("pramjati02/t5-base-trained")
model_t5 = AutoModelForSeq2SeqLM.from_pretrained("pramjati02/t5-base-trained").to(device)

tokenizer_pegasus = AutoTokenizer.from_pretrained("pramjati02/pegasus-large-trained")
model_pegasus = AutoModelForSeq2SeqLM.from_pretrained("pramjati02/pegasus-large-trained").to(device)