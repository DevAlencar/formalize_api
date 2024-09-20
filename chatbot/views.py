from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import requests
from .serializers import MessageSerializer


class ChatbotView(APIView):

    def post(self, request):
        serializer = MessageSerializer(data=request.data)

        if serializer.is_valid():
            user_message = serializer.validated_data['message']

            # Enviar a mensagem para o Rasa
            rasa_url = "http://localhost:5005/webhooks/rest/webhook"
            payload = {
                "sender": "web_user",  # Um identificador único para o usuário
                "message": user_message
            }

            try:
                rasa_response = requests.post(rasa_url, json=payload)
                rasa_response_json = rasa_response.json()

                # Retornar a resposta do Rasa para o frontend
                if rasa_response_json:
                    bot_message = rasa_response_json[0].get('text', "Desculpe, não entendi.")
                    return Response({"response": bot_message}, status=status.HTTP_200_OK)
                else:
                    return Response({"response": "Nenhuma resposta disponível."}, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"error": "Erro ao conectar com o servidor Rasa."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
