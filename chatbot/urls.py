from django.urls import path
from .views import ChatBotView, ChatBotPageView

urlpatterns = [
    path('', ChatBotView.as_view(), name='chatbot'),
    path('chat/', ChatBotPageView.as_view(), name='chat_page'), #Rota para o HTML
]
