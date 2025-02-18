from abc import ABC, abstractmethod

class AssistantModel(ABC):
    def __init__(self, model_name: str):
        super().__init__()
        self.model_name = model_name

    @abstractmethod
    def generate_response(self, prompt: str)->str:
        pass

    @abstractmethod
    def generate_diagnose_prompt(self, patient: 'Patient'):
        pass
    
    @abstractmethod
    def generate_summary_prompt(self, patient: 'Patient'):
        pass