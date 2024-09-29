# chatbot/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render

class ChatBotView(APIView):
    state_links = {
        "São Paulo": "https://www.jucesp.sp.gov.br/",
        "Rio de Janeiro": "http://www.jucerja.rj.gov.br/",
        "Minas Gerais": "https://www.jucemg.mg.gov.br/",
        "Bahia": "http://www.juceb.ba.gov.br/",
        "Paraná": "http://www.juntacomercial.pr.gov.br/",
        "Rio Grande do Sul": "https://www.jucisrs.rs.gov.br/",
    }

    predefined_responses = {
        "Oi": "Olá! Eu sou o Assistente de Abertura de CNPJ. Como posso te ajudar?",
        "Qual o primeiro passo para abrir um CNPJ?": (
            "O primeiro passo para abrir um CNPJ é acessar o site da Receita Federal "
            "e iniciar o processo de inscrição: https://www.gov.br/receitafederal/pt-br. "
            "Depois, é necessário consultar a Junta Comercial do seu estado."
        ),
        "Como abrir um CNPJ?": (
            "Para abrir um CNPJ, você deve seguir os seguintes passos:\n"
            "1. Definir a natureza jurídica da empresa.\n"
            "2. Fazer o registro na Junta Comercial do seu estado.\n"
            "3. Realizar a inscrição no site da Receita Federal.\n"
            "Quer saber mais sobre como proceder no seu estado?"
        ),
        "Quais documentos são necessários para abrir um CNPJ?": (
            "Os documentos básicos são:\n"
            "1. Documento de identidade do titular.\n"
            "2. Comprovante de residência.\n"
            "3. Contrato social da empresa.\n"
            "Alguns estados podem exigir documentos adicionais. Consulte a Junta Comercial do seu estado."
        ),
        "Quais são os tipos de empresa?": (
            "Os tipos de empresa mais comuns são:\n"
            "1. MEI (Microempreendedor Individual)\n"
            "2. EIRELI (Empresa Individual de Responsabilidade Limitada)\n"
            "3. LTDA (Sociedade Limitada)\n"
            "4. Sociedade Anônima (SA)\n"
            "Cada tipo tem vantagens e desvantagens. Qual estado você está interessado?"
        ),
        "Adeus": "Até logo! Espero ter ajudado com seu processo de abertura de CNPJ."
    }

    def post(self, request, *args, **kwargs):
        user_input = request.data.get("mensagem", "")

        # Verificando se o usuário mencionou um estado
        for estado, link in self.state_links.items():
            if estado.lower() in user_input.lower():
                resposta = (
                    f"Para abrir um CNPJ no estado de {estado}, você deve visitar a Junta Comercial "
                    f"no seguinte link: {link}."
                )
                return Response({"resposta": resposta}, status=status.HTTP_200_OK)

        resposta = self.predefined_responses.get(
            user_input,
            "Desculpe, não entendi. Você pode perguntar sobre como abrir um CNPJ ou documentos necessários."
        )

        return Response({"resposta": resposta}, status=status.HTTP_200_OK)

class ChatBotPageView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'chatbot/index.html')