from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained("pramjati02/Bart-Base-Trained")
model = AutoModelForSeq2SeqLM.from_pretrained("pramjati02/Bart-Base-Trained").to(device)

