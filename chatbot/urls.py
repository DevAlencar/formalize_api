from django.urls import path
from .views import ChatBotView, ChatBotPageView

urlpatterns = [
    path('v1/', ChatBotView.as_view(), name='chatbot'),
    path('chat/', ChatBotPageView.as_view(), name='chat_page'), #Rota para o HTML
]
