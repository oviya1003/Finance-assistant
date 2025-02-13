from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load the fine-tuned model
model_path = r"C:\Users\Sheid_heda\Desktop\Oviya\fine_tune_t5.py"  # Replace with your actual model path
tokenizer = T5Tokenizer.from_pretrained(model_path)
model = T5ForConditionalGeneration.from_pretrained(model_path)

# Test the model
def generate_answer(question, context):
    input_text = f"question: {question} context: {context}"
    inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs.input_ids, max_length=50, num_beams=5, early_stopping=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Example usage
question = "What are the best investment options for high-risk tolerance?"
context = "High-risk investments include stocks, cryptocurrencies, and equity funds."
print(generate_answer(question, context))
