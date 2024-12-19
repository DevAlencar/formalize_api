# chatbot/state_handlers/sefaz.py
from .base import BaseState
from ..states import ChatState, StateResponse
from ..data import SEFAZ_LINKS

class SefazState(BaseState):
    def handle(self, user_input: str) -> StateResponse:
        if user_input == "Desejo retornar ao menu inicial":
            return self.create_response(
                "Voltando ao menu inicial",
                ["Abrir CNPJ", "Emitir certidões"],
                ChatState.MENU
            )

        link = SEFAZ_LINKS.get(user_input, "Link não encontrado")
        
        if link != "Link não encontrado":
            return self.create_response(
                f"Aqui está o link para emitir a Certidão da SEFAZ no estado de {user_input}: {link}.\n\n" "O que deseja fazer agora?",
                ["Desejo retornar ao menu inicial", "Desejo tentar outro estado"],
                ChatState.MENU
            )

        estados = list(SEFAZ_LINKS.keys())
        return self.create_response(
            "Estado não encontrado. Por favor, escolha um dos estados abaixo:",
            estados + ["Desejo retornar ao menu inicial"],
            ChatState.CERTIDAO_SEFAZ
        )