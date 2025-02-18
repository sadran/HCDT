from .chatgpt import ChatGPTModel
from .medllama import MedLlamaModel

MODEL_NAMES_DICT = {'gpt-4': ChatGPTModel, 
                    'johnsnowlabs/JSL-MedLlama-3-8B-v2.0': MedLlamaModel}
