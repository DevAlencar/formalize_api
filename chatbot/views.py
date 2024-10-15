from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .state_machine import ChatBotStateMachine

class ChatBotView(APIView):

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        user_input = request.data.get("mensagem", "")
        
        # Recupera o estado atual da sessão ou inicia com 'start'
        state = request.session.get('chatbot_state', 'start')
        
        # Inicializa a máquina de estados com o estado atual
        bot = ChatBotStateMachine(state)
        
        # Processa o input e gera a resposta de acordo com o estado
        resposta, new_state = bot.handle_flow(user_input)
        
        # Atualiza o estado na sessão
        request.session['chatbot_state'] = new_state
        
        return Response({"resposta": resposta}, status=status.HTTP_200_OK)
