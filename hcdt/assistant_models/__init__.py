from .chatgpt import ChatGPTModel
from .medllama3 import MedLlama3Model
from .medllama2 import MedLlama2Model

MODEL_NAMES_DICT = {'gpt-4': ChatGPTModel, 
                    'medllama3': MedLlama3Model,
                    'medllama2' : MedLlama2Model }
