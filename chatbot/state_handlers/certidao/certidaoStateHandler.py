from chatbot.state_handlers.base import BaseState, StateResponse, ChatState
from chatbot.data import MENU_OPTIONS


class certidaoStateHandler(BaseState):
          
    def handle(self, user_input: str) -> StateResponse:

        if '1' in user_input:
            return self.create_response(
                "Escolha uma das opções abaixo:",
                MENU_OPTIONS['main'],
                ChatState.CERTIDAO_STATE_HANDLER
            )
        elif '2' in user_input:
            return self.create_response(
                "Escolha uma das opções abaixo:",
                MENU_OPTIONS['certidoes'],
                ChatState.EXPLAIN_CERTIDOES
            )   
        return self.create_response(
            "Informe uma opção válida.",
                ["Desejo retornar ao menu inicial", "Desejo tentar outro estado"],
                ChatState.CERTIDAO_STATE_HANDLER
        )
            