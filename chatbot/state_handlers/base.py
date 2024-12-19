# chatbot/state_handlers/base.py
from abc import ABC, abstractmethod
from ..states import StateResponse, ChatState, Question

class BaseState(ABC):
    @abstractmethod
    def handle(self, user_input: str) -> StateResponse:
        pass
    
    def create_response(self, answer: str, questions: list, next_state: ChatState) -> StateResponse:
        return StateResponse(
            answer=answer,
            questions=[Question(body=q) for q in questions],
            next_state=next_state
        )
