# chatbot/state_handlers/certidoes.py
from typing import Dict
from .base import BaseState
from ..states import ChatState, StateResponse
from ..data import CERTIDOES_LINKS, MENU_OPTIONS

class ExplainCertidoesState(BaseState):
    def handle(self, user_input: str) -> StateResponse:
        certidoes: Dict[str, tuple] = {
            '1': ('receita_federal', 'Certidão da Receita Federal'),
            '2': ('sefaz', 'Certidão da SEFAZ (ICMS)'),
            '3': ('regularidade_fiscal', 'Certidão de Regularidade Fiscal'),
            '4': ('fgts', 'Certidão FGTS'),
            '5': ('trabalhista', 'Certidão Trabalhista'),
            '6': ('municipal', 'Certidão Municipal'),
            '7': ('antecedentes', 'Certidão de Antecedentes Criminais'),
            '8': ('antecedentes_criveis', 'Antecedentes Criveis')
        }

        if user_input in certidoes:
            cert_key, cert_name = certidoes[user_input]
            
            if cert_key == 'sefaz':
                return self.create_response(
                    "Informe o estado que deseja buscar:",
                    ["Desejo retornar ao menu inicial"],
                    ChatState.CERTIDAO_SEFAZ
                )
            
            link = CERTIDOES_LINKS.get(cert_key, '')
            return self.create_response(
                f"Aqui está o link para emitir a {cert_name}: {link}",
                ["Desejo retornar ao menu inicial"],
                ChatState.MENU
            )
            
        return self.create_response(
            "Opção inválida. Escolha uma das opções abaixo:",
            MENU_OPTIONS['certidoes'],
            ChatState.EXPLAIN_CERTIDOES
        )