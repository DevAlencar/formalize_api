# chatbot/state_handlers/sefaz.py
from .base import BaseState
from ..states import ChatState, StateResponse
from ..data import SEFAZ_LINKS

class SefazState(BaseState):
    def handle(self, user_input: str) -> StateResponse:
        estados = list(SEFAZ_LINKS.keys())
        print(estados)
        
        estadoEscolhido = estados[int(user_input) - 1]
        print(estadoEscolhido)
        if estadoEscolhido in SEFAZ_LINKS:
            return self.create_response(
                f"O link para a SEFAZ de {estadoEscolhido} é: {SEFAZ_LINKS[estadoEscolhido]}",
                ["Desejo retornar ao menu inicial", "Desejo tentar uma outra certidão"],
                ChatState.CERTIDAO_STATE_HANDLER
            )

        return self.create_response(
            "Não encontrado. Por favor, escolha um dos estados abaixo:",
            estados + ["Desejo retornar ao menu inicial"],
            ChatState.CERTIDAO_SEFAZ
        )