
# chatbot/state_machine.py
from typing import Dict, Type
from .states import ChatState, StateResponse
from .state_handlers.certidao.certidaoStateHandler import certidaoStateHandler
from .state_handlers.base import BaseState
from .state_handlers.menu import MenuState
from .state_handlers.certidao.certidoes import ExplainCertidoesState
from .state_handlers.sefaz import SefazState

class ChatBotStateMachine:
    def __init__(self):
        self._states: Dict[ChatState, Type[BaseState]] = {
            ChatState.MENU: MenuState,
            ChatState.EXPLAIN_CERTIDOES: ExplainCertidoesState,
            ChatState.CERTIDAO_SEFAZ: SefazState,
            ChatState.CERTIDAO_STATE_HANDLER: certidaoStateHandler,
        }
        self.current_state = ChatState.MENU
    
    def get_menu_options(self) -> StateResponse:
        menu_state = MenuState()
        return menu_state.handle("")
        
    def handle_flow(self, user_input: str) -> StateResponse:
        try:
            state_handler = self._states[self.current_state]()
            response = state_handler.handle(user_input)
            self.current_state = response.next_state
            return response
        
        except Exception as e:
            menu_response = self.get_menu_options()
            return StateResponse(
                answer="Desculpe, ocorreu um erro. Voltando ao menu inicial.\n\n" + menu_response.answer,
                questions=menu_response.questions,
                next_state=ChatState.MENU
            )

