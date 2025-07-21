Some model training and testing scripts may have forward passes with "autocast()". 
This is a method called Mixed Precision, which reduces some of the forward pass calculations from 32float to 16float, making them more efficient in training.
This did not work for BART and PEGASUS, and have been removed in the current iteration of training models (which are still training).
Updated model scripts will be uploaded once training has been finalized. 
