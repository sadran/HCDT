#from openai import OpenAI

class ChatGPTModel:
    def __init__(self, model="gpt-4"):
        self.api_key = ""
        self.model = model
        #self.client = OpenAI(api_key=self.api_key)
        self.client = None
    def diagnose(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=prompt
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error: {e}"
        
    def summarize(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=prompt
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error: {e}"

    def generate_diagnose_prompt(self, patient):
        return [{"role": "system", "content": "You are a medical AI diagnosing patients based on EHR."}, 
                {"role": "user", "content": f"Based on the following patient history, provide a diagnosis and potential treatment options:\n\n{patient}"}]
    
    def generate_summary_prompt(self, patient):
        return [{"role": "system", "content": "You are a medical AI summarizing patient data."}, 
                {"role": "user", "content": f"Summarize the patient data for patient: {patient}"}]