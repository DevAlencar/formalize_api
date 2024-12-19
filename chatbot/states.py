# chatbot/states.py
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional

class ChatState(Enum):
    MENU = "menu"
    EXPLAIN_CERTIDOES = "explain_certidoes" 
    CERTIDAO_SEFAZ = "certidao_sefaz"
    START_CNPJ = "start_cnpj_process"
    CERTIDAO_STATE_HANDLER = "certidao_state_handler"

@dataclass
class Question:
    body: str

@dataclass
class StateResponse:
    answer: str
    questions: List[Question]
    next_state: ChatState
