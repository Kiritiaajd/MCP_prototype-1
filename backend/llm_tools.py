from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
import re
import json

class LocalLLMParser:
    def __init__(self, model_name='distilgpt2'):
        print("Loading local distilGPT2 model...")
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token  # <---- Add this line
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.model.eval()


    def parse_query(self, query: str) -> dict:
        """
        Given a user query, generate a structured JSON-like string, then extract data heuristically.
        """

        prompt = (
            "You are a financial assistant. Extract the following information from user queries:\n"
            "- entity: company or organization mentioned\n"
            "- fields: financial terms or metrics asked\n"
            "- dataset: 'tat' if TAT-related, 'loan' if loan/credit-related\n\n"
            "Examples:\n"
            "Query: What is the TAT score of ABC Ltd?\n"
            "{\n  \"entity\": \"ABC Ltd\",\n  \"fields\": [\"TAT score\"],\n  \"dataset\": \"tat\" }\n\n"
            "Query: Show the loan amount and credit status for XYZ Corp\n"
            "{\n  \"entity\": \"XYZ Corp\",\n  \"fields\": [\"loan amount\", \"credit status\"],\n  \"dataset\": \"loan\" }\n\n"
            f"Query: {query}\n"
            "Response:\n"
        )

        # Use tokenizer with attention_mask
        inputs = self.tokenizer(prompt, return_tensors='pt', padding=True, truncation=True)
        input_ids = inputs["input_ids"]
        attention_mask = inputs["attention_mask"]

        with torch.no_grad():
            outputs = self.model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                max_length=input_ids.shape[1] + 100,
                num_return_sequences=1,
                no_repeat_ngram_size=2,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                eos_token_id=self.tokenizer.eos_token_id
            )

        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract the JSON substring from generated text using regex
        json_match = re.search(r'\{.*?\}', generated_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            try:
                parsed = json.loads(json_str)
                return parsed
            except Exception as e:
                print(f"Failed to parse JSON from generated output: {e}")
                print("Generated text:", json_str)
                return {}
        else:
            print("No JSON found in model output.")
            print("Model output:", generated_text)
            return {}

if __name__ == "__main__":
    parser = LocalLLMParser()
    test_query = "What is the TAT score and credit status of XYZ Enterprises?"
    result = parser.parse_query(test_query)
    print("Parsed output:", result)
