from transformers import pipeline

# Test loading the T5 model
qa_model = pipeline("question-answering", model="t5-small", tokenizer="t5-small")
print("T5 Model Loaded Successfully!")
