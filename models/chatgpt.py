import openai

class ChatGPTModel:
    def __init__(self, model="gpt-4"):
        self.api_key = None
        self.model = model
        openai.api_key = self.api_key  # Set API key

    def diagnose(self, prompt):
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=prompt
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error: {e}"