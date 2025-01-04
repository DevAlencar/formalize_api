# chatbot/state_handlers/menu.py
from .base import BaseState
from ..states import ChatState, StateResponse
from ..data import MENU_OPTIONS

class MenuState(BaseState):
    def get_initial_options(self) -> StateResponse:
        return self.create_response(
            "Escolha uma das opções abaixo:",
            MENU_OPTIONS['main'],
            ChatState.MENU
        )
        
    def handle(self, user_input: str) -> StateResponse:
        if not user_input:# Se não houver input, retorna menu inicial
            return self.get_initial_options()

        if '1' in user_input:
            return self.create_response(
                "Para abrir um CNPJ, você deve seguir os seguintes passos:",
                [
                    "Definir a natureza jurídica da empresa",
                    "Fazer o registro na Junta Comercial do seu estado",
                    "Realizar a inscrição no site da Receita Federal", 
                    "Deseja saber mais sobre algum estado específico?",
                    "Deseja voltar ao menu inicial?"
                ],
                ChatState.START_CNPJ
            )
        elif '2' in user_input:
            print("Entrou no 2")
            return self.create_response(
                "Existem várias certidões negativas que podem ser emitidas, sobre qual deseja saber mais?",
                MENU_OPTIONS['certidoes'],
                ChatState.EXPLAIN_CERTIDOES
            )
        return self.create_response(
            "Opção inválida. Por favor escolha uma opção válida:",
            MENU_OPTIONS['main'],
            ChatState.MENU
        )
