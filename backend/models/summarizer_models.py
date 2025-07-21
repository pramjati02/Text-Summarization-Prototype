from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained("bart_base_trained")
model = AutoModelForSeq2SeqLM.from_pretrained("bart_base_trained").to(device)

