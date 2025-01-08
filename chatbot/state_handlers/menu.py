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
                "Ótimo! Acesse o link a seguir para prosseguir com a abertura de CNPJ: https://www.gov.br/empresas-e-negocios/pt-br/empreendedor/quero-abrir-um-negocio/como-abrir-uma-empresa",
                [
                    "Desejo voltar ao menu inicial."
                ],
                ChatState.START_CNPJ
            )
        elif '2' in user_input:
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
