from .base import AssistantModel
import torch
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer

class MedLlamaModel(AssistantModel):
    def __init__(self, config):
        super().__init__(config['model_name'])
        # Set device
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(config['model_local_path'], local_files_only=True)
        # Load model with precision and device mapping
        self.model = AutoModelForCausalLM.from_pretrained(
            config['model_local_path'],
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto",
            local_files_only=True)

        # Set model to evaluation mode
        self.model.eval()

    def generate_diagnose_prompt(self, patient):
        return [{"role": "system", "content": "You are a medical AI diagnosing patients based on EHR."}, 
                {"role": "user", "content": f"Based on the following patient history, provide a diagnosis and potential treatment options:\n\n{patient}"}]

    def generate_summary_prompt(self, patient):
        return [{"role": "system", "content": "You are a medical AI summarizing patient data."}, 
                {"role": "user", "content": f"Summarize the patient data for patient: {patient}"}]

    def generate_response(self, prompt):
        ## Tokenize input text
        #inputs = self.tokenizer(prompt, return_tensors="pt")
        ## Generate response
        #with torch.no_grad():
        #    outputs = self.model.generate(
        #        **inputs,
        #        max_new_tokens=self.config['max_new_tokens'],
        #        do_sample=self.config['do_samples'],
        #        temperature=self.config['temperature'],
        #        top_k=self.config['top_k'],
        #        top_p=self.config['top_p'],
        #    )
        # Decode and return the generated text
        #return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        prompt = self.tokenizer.apply_chat_template(prompt, tokenize=False, add_generation_prompt=True)
        pipeline = transformers.pipeline(
            "text-generation",
            model=self.config['model_local_path'],
            torch_dtype=torch.float16,
            device_map="auto",
            )
        outputs = pipeline(prompt, max_new_tokens=self.config['max_new_tokens'],
                           do_sample=self.config['do_samples'],
                           temperature=self.config['temperature'],
                           top_k=self.config['top_k'],
                           top_p=self.config['top_p'])
        return outputs[0]["generated_text"]