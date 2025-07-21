import torch
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, DataCollatorForSeq2Seq
from datasets import load_dataset
from carbontracker.tracker import CarbonTracker
from tqdm import tqdm
from torch.nn.utils.rnn import pad_sequence
from torch.optim import AdamW
from torch.cuda.amp import autocast, GradScaler
import evaluate 
import nltk
nltk.download('punkt')

# Initalizing ROUGE and BERT score metrics
rouge = evaluate.load("rouge")
bertscore = evaluate.load("bertscore")

# Loading the datasets 
print("loading testing set...")
raw_test = torch.load("/cs/home/psxpj10/dissertation/raw_test_25percent.pt")
    
print("datasets loaded")
# Load model (CHANGE THIS)
model = AutoModelForSeq2SeqLM.from_pretrained("./pegasus-large-trained").to("cuda") # Using CPU but if GPU add .to("cuda")
tokenizer = AutoTokenizer.from_pretrained("./pegasus-large-trained") 

# Define the tokenizer-aware preprocessing
def preprocess(example):
    # Tokenize the article as input
    inputs = tokenizer(
        example["article"], max_length=800, padding="max_length", truncation=True, return_tensors="pt"
    )
    # Tokenize the abstract as the target/label
    targets = tokenizer(
        example["abstract"], max_length=256, padding="max_length", truncation=True, return_tensors="pt"
    )
    # Return a dictionary with input tensors for training
    return {
        "input_ids": inputs["input_ids"].squeeze(0),
        "attention_mask": inputs["attention_mask"].squeeze(0),
        "labels": targets["input_ids"].squeeze(0),
    }


# tokenize the datasets 
print("pre-processing the dataset")
processed_test = [preprocess(x) for x in raw_test]
print("pre-processing done")

print("wrapping datasets into dataloaders...")
# Wrap datasets in DataLoaders for batching and collate into tensors

data_collator = DataCollatorForSeq2Seq(tokenizer, model=model, padding="longest")

# Wrap datasets in DataLoaders for batching
dataloader = DataLoader(processed_test, batch_size=4, collate_fn=data_collator)

model.eval()  # Set to eval mode
sample_outputs = []

# Only generate for a few samples to inspect
for batch in tqdm(dataloader):
    # Move input tensors to GPU
    input_ids = batch["input_ids"].to("cuda")
    attention_mask = batch["attention_mask"].to("cuda")

    # Generate summaries (can change max_length/num_beams/etc. as needed)
    with torch.no_grad():
        with autocast():  # using mixed precision
            generated_ids = model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                max_length=256,
                num_beams=4,      # considers top 4 summaries and chooses the best one 
                early_stopping=True
            )

    # Decode summaries and references
    decoded_preds = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
    decoded_refs = tokenizer.batch_decode(batch["labels"], skip_special_tokens=True)

    # Store for printing/eval
    sample_outputs.extend(zip(decoded_preds, decoded_refs))

    #if len(sample_outputs) >= 5:  # Stop after 5 examples
    #    break

# obtaining all predicted and reference summaries
all_preds = [pred for pred, ref in sample_outputs]
all_refs = [ref for pref, ref in sample_outputs]

# computing ROUGE Scores 
rouge_scores = rouge.compute(predictions=all_preds, references=all_refs)
print("\nROUGE Scores:", rouge_scores)

bert_scores = bertscore.compute(predictions=all_preds, references=all_refs, lang="en")
print("\nBERTScore F1 (average):", sum(bert_scores["f1"]) / len(bert_scores["f1"]) )

# Print five example outputs
for i, (pred, ref) in enumerate(sample_outputs[:5]):
    print(f"Summary {i+1}")
    print(f"Generated Summary:\n{pred.strip()}")
    print(f"Reference Summary:\n{ref.strip()}")