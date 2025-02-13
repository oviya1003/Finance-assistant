import pandas as pd
from datasets import Dataset
from transformers import T5ForConditionalGeneration, T5Tokenizer, Trainer, TrainingArguments

# Load the dataset
df = pd.read_csv('C:/Users/Sheid_heda/Desktop/Oviya/FINQ&A.csv')

# Prepare the dataset
data = Dataset.from_pandas(df[['Question', 'Answer']])  # Adjust column names if necessary

# Load pre-trained T5 model and tokenizer
model_name = "t5-small"  # You can change this to a larger model if needed
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

# Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(examples['question'], padding="max_length", truncation=True, max_length=128)

tokenized_datasets = data.map(tokenize_function, batched=True)

# Define the training arguments
training_args = TrainingArguments(
    output_dir='./results',          
    evaluation_strategy="epoch",     
    learning_rate=2e-5,             
    per_device_train_batch_size=8,  
    per_device_eval_batch_size=8,   
    num_train_epochs=3,            
    weight_decay=0.01,              
)

# Initialize the Trainer
trainer = Trainer(
    model=model,                         
    args=training_args,                  
    train_dataset=tokenized_datasets,         
    eval_dataset=tokenized_datasets,            
)

# Fine-tune the model
trainer.train()

# Save the fine-tuned model
model.save_pretrained('C:/Users/Sheid_heda/Desktop/Oviya/finetuned_model')
tokenizer.save_pretrained('C:/Users/Sheid_heda/Desktop/Oviya/finetuned_model')
