from django.shortcuts import render
# chatbot/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .state_machine import ChatBotStateMachine
from .states import ChatState
from django.utils import timezone
from django.conf import settings
from .states import ChatState

class ChatBotView(APIView):
    def get(self, request):
        # Clear previous session data on new chat
        if 'chatbot_state' in request.session:
            del request.session['chatbot_state']
        
        bot = ChatBotStateMachine()
        response = bot.handle_flow("")
        request.session['last_activity'] = timezone.now().isoformat()
        request.session['chatbot_state'] = ChatState.MENU.value
        return Response({
            "answer": response.answer,
            "questions": [{"body": q.body} for q in response.questions]
        })


    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        current_time = timezone.now()
        
        # Check if session exists and has required data
        if not request.session.get('last_activity') or not request.session.get('chatbot_state'):
            # Session expired or missing
            return Response({
                "answer": "Sua sessão expirou. Por favor, recarregue a página para iniciar uma nova conversa.",
                "questions": []
            }, status=status.HTTP_200_OK)
        
        # Session exists, check timeout
        last_activity = request.session['last_activity']
        last_activity_time = timezone.datetime.fromisoformat(last_activity)
        time_diff = (current_time - last_activity_time).seconds
        
        if time_diff > settings.SESSION_COOKIE_AGE:
            request.session.flush()
            return Response({
                "answer": "Sua sessão expirou. Por favor, recarregue a página para iniciar uma nova conversa.",
                "questions": []
            }, status=status.HTTP_200_OK)
        
        # Continue with normal flow...
        user_input = request.data.get("mensagem", "")
        bot = ChatBotStateMachine()
        bot.current_state = ChatState(request.session['chatbot_state'])
        
        response = bot.handle_flow(user_input)
        request.session['chatbot_state'] = response.next_state.value
        request.session['last_activity'] = current_time.isoformat()
        
        return Response({
            "answer": response.answer,
            "questions": [{"body": q.body} for q in response.questions]
        }, status=status.HTTP_200_OK)


class ChatBotPageView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'chatbot/index.html')