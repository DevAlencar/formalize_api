from ..base import BaseState
from ...states import ChatState, StateResponse
from ...data import MENU_OPTIONS

class StartCNPJState(BaseState):
    
    def handle(self, user_input: str) -> StateResponse:
        
        return self.create_response(
            "Escolha uma das opções abaixo:",
            MENU_OPTIONS['main'],
            ChatState.MENU
        )