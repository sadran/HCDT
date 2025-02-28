from .base import AssistantModel
import requests

class MedLlama2Model(AssistantModel):
    def __init__(self, config):
        super().__init__(config['model_name'])
        self.api_url = config['api_url']


    def generate_response(self, prompt: str) -> str:
        """Generate a response from MedLlama2 for a given prompt."""
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(self.api_url, json=payload)
        if response.status_code == 200:
            return response.json().get("response", "No response from model.")
        else:
            return f"Error: {response.status_code}, {response.text}"

    def generate_prompt(self, system_message, user_message, response_template) -> str:
        """Generate a prompt for MedLlama2."""
        message = '\n'.join([system_message, user_message, "Respond strictly in this JSON format:", f"{response_template}"])
        return message