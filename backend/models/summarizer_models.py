from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

"""
# Check if torch is using cuda 
print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("CUDA device name:", torch.cuda.get_device_name(0))
"""

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer_bart = AutoTokenizer.from_pretrained("./models/bart_base_trained")
model_bart = AutoModelForSeq2SeqLM.from_pretrained("./models/bart_base_trained").to(device)

tokenizer_t5 = AutoTokenizer.from_pretrained("./models/t5_base_trained")
model_t5 = AutoModelForSeq2SeqLM.from_pretrained("./models/t5_base_trained").to(device)

tokenizer_pegasus = AutoTokenizer.from_pretrained("./models/pegasus_large_trained")
model_pegasus = AutoModelForSeq2SeqLM.from_pretrained("./models/pegasus_large_trained").to(device)