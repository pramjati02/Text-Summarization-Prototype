import torch
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, DataCollatorForSeq2Seq
from datasets import load_dataset
from carbontracker.tracker import CarbonTracker
from tqdm import tqdm
from torch.nn.utils.rnn import pad_sequence
from torch.optim import AdamW
from torch.cuda.amp import autocast, GradScaler

# Loading the datasets 
raw_train = torch.load("/cs/home/psxpj10/dissertation/raw_train_25percent.pt")
raw_val = torch.load("/cs/home/psxpj10/dissertation/raw_val_25percent.pt")
    
# Load model (T5 base) (CHANGE THIS)
model = AutoModelForSeq2SeqLM.from_pretrained("./pegasus-large").to("cuda") # Using CPU but if GPU add .to("cuda")
tokenizer = AutoTokenizer.from_pretrained("./pegasus-large") 

# Define the tokenizer-aware preprocessing
def preprocess(example):
    # Tokenize the article as input, set input max_length to 512 as is standard for training T5 models
    inputs = tokenizer(
        example["article"], max_length=800, padding="max_length", truncation=True, return_tensors="pt"
    )
    # Tokenize the abstract as the target/label
    targets = tokenizer(
        example["abstract"], max_length=256, padding="max_length", truncation=True, return_tensors="pt"
    )
    
    labels = targets["input_ids"]
    labels = torch.where(labels == tokenizer.pad_token_id, -100, labels)  # mask padding tokens
    
    # Return a dictionary with input tensors for training
    return {
        "input_ids": inputs["input_ids"].squeeze(0),
        "attention_mask": inputs["attention_mask"].squeeze(0),
        "labels": labels.squeeze(0),
    }


# tokenize the datasets 
print("pre-processing the dataset")
processed_train = [preprocess(x) for x in raw_train]
processed_val = [preprocess(x) for x in raw_val]
print("pre-processing done")

print("wrapping datasets into dataloaders and initilizing model paramters...")
# Wrap datasets in DataLoaders for batching and collate into tensors

data_collator = DataCollatorForSeq2Seq(tokenizer, model=model, padding="longest")

# Wrap datasets in DataLoaders for batching
dataloader = DataLoader(processed_train, batch_size=4, collate_fn=data_collator)
val_dataloader = DataLoader(processed_val, batch_size=4, collate_fn=data_collator)

# Set up the optimizer (use AdamW from torch.optim)
optimizer = AdamW(model.parameters(), lr=2e-5)

# set number of epochs during training 
num_epochs = 6

# Initialize CarbonTracker to measure emissions/energy usage
tracker = CarbonTracker(epochs=num_epochs, components="gpu", monitor_epochs = -1, log_dir = "./carbon-results-pegasus")

# initializing gradient scaling for less memory usage (part of mixed precision)
#scaler = GradScaler()

print("Beginning model training...")
# Training loop for 3 epochs
for epoch in range(num_epochs):
    print(f"\nEpoch {epoch + 1}/{num_epochs}")
    tracker.epoch_start()  # Start CarbonTracker measurement for the epoch

    model.train()
    total_loss = 0  # Track total loss to calculate average

    # Iterate over each batch in the training set
    for batch in tqdm(dataloader):
        # Commented out GPU transfer for CPU-only usage
        # input_ids = batch["input_ids"].to("cuda")
        # attention_mask = batch["attention_mask"].to("cuda")
        # labels = batch["labels"].to("cuda")

        input_ids = batch["input_ids"].to("cuda")
        attention_mask = batch["attention_mask"].to("cuda")
        labels = batch["labels"].to("cuda")

        # Forward pass without mixed precision 
        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss  # Compute loss

        # Backward pass and optimization
        loss.backward()
        optimizer.step()
        #scaler.update()
        optimizer.zero_grad()

        # Accumulate loss for logging
        total_loss += loss.item()

    # Calculate and print average training loss for this epoch
    avg_loss = total_loss / len(dataloader)
    print(f"Average training loss: {avg_loss:.4f}")

    # Validation loop
    model.eval()
    val_loss = 0
    with torch.no_grad():
        for batch in tqdm(val_dataloader):
            # input_ids = batch["input_ids"].to("cuda")
            # attention_mask = batch["attention_mask"].to("cuda")
            # labels = batch["labels"].to("cuda")

            input_ids = batch["input_ids"].to("cuda")
            attention_mask = batch["attention_mask"].to("cuda")
            labels = batch["labels"].to("cuda")

            # validation loop 
            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            val_loss += outputs.loss.item()

    avg_val_loss = val_loss / len(val_dataloader)
    print(f"Average validation loss: {avg_val_loss:.4f}")

    tracker.epoch_end()  # End CarbonTracker measurement for the epoch

# Stop the CarbonTracker once training is finished
tracker.stop()

# Save model and tokenizer to a folder (CHANGE THIS)
model.save_pretrained("./pegasus-large-trained")
tokenizer.save_pretrained("./pegasus-large-trained")