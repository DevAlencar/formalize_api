
# chatbot/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .state_machine import ChatBotStateMachine
from .states import ChatState

class ChatBotView(APIView):
    def get(self, request):
        bot = ChatBotStateMachine()
        response = bot.handle_flow("")
        return Response({
            "answer": response.answer,
            "questions": [{"body": q.body} for q in response.questions]
        })

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        user_input = request.data.get("body", "")
        
        bot = ChatBotStateMachine()
        if 'chatbot_state' in request.session:
            bot.current_state = ChatState(request.session['chatbot_state'])
            
        response = bot.handle_flow(user_input)
        request.session['chatbot_state'] = response.next_state.value
        
        return Response({
            "answer": response.answer,
            "questions": [{"body": q.body} for q in response.questions]
        }, status=status.HTTP_200_OK)