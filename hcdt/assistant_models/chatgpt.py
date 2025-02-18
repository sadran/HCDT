import openai
from .base import AssistantModel

class ChatGPTModel(AssistantModel):
    def __init__(self,config):
        super().__init__(config['model_name'])
        self.api_key = config['api_key']
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

    def generate_diagnose_prompt(self, patient):
        return [{"role": "system", "content": "You are a medical AI diagnosing patients based on EHR."}, 
                {"role": "user", "content": f"Based on the following patient history, provide a diagnosis and potential treatment options:\n\n{patient}"}]
    
    def generate_summary_prompt(self, patient):
        return [{"role": "system", "content": "You are a medical AI summarizing patient data."}, 
                {"role": "user", "content": f"Summarize the patient data for patient: {patient}"}]