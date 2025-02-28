from abc import ABC, abstractmethod

class AssistantModel(ABC):
    def __init__(self, model_name: str):
        super().__init__()
        self.model_name = model_name

    @abstractmethod
    def generate_response(self, prompt: str)->str:
        pass
    
    @abstractmethod
    def generate_prompt(self, system_message, user_message, response_template )->str:
        pass
