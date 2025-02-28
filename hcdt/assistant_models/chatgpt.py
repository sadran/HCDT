import openai
from .base import AssistantModel

class ChatGPTModel(AssistantModel):
    def __init__(self,config):
        super().__init__(config['model_name'])
        with open(config['api_key_path'], 'r') as file:
            self.api_key = file.read().strip()
        openai.api_key = self.api_key
        self.client = openai
        
    def generate_response(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=prompt
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {e}"

    def generate_prompt(self, system_message, user_message, response_template):
        system_message = '\n'.join([system_message, 'Provide your answer in JSON structure like this:', f"{response_template}"])
        messages = [{"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}]
        return messages