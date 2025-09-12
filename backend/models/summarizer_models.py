from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer_bart = AutoTokenizer.from_pretrained("./models/bart_base_trained")
model_bart = AutoModelForSeq2SeqLM.from_pretrained("./models/bart_base_trained").to(device)

tokenizer_t5 = AutoTokenizer.from_pretrained("./models/t5_base_trained")
model_t5 = AutoModelForSeq2SeqLM.from_pretrained("./models/t5_base_trained").to(device)

tokenizer_pegasus = AutoTokenizer.from_pretrained("./models/pegasus_large_trained")
model_pegasus = AutoModelForSeq2SeqLM.from_pretrained("./models/pegasus_large_trained").to(device)