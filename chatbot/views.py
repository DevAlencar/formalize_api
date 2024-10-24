from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .state_machine import ChatBotStateMachine

class ChatBotView(APIView):
    def get(self,request):
        answer = "Olá! Escolha uma das opções abaixo para continuar:"
        questions = [
            {"body": "Abrir CNPJ"},
            {"body": "Emitir certidões"}
        ]
        return Response({"answer": answer, "questions": questions})

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        user_input = request.data.get("mensagem", "")
        
        # Recupera o estado atual da sessão ou inicia com 'start'
        state = request.session.get('chatbot_state', 'menu')
        
        # Inicializa a máquina de estados com o estado atual
        bot = ChatBotStateMachine(state)
        
        # Processa o input e gera a resposta de acordo com o estado
        answer, questions, new_state = bot.handle_flow(user_input)
        
        # Atualiza o estado na sessão
        request.session['chatbot_state'] = new_state
        
        return Response({"answer": answer, "questions": questions}, status=status.HTTP_200_OK)