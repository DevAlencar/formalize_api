from django.urls import path
from .views import ChatBotView

urlpatterns = [
    path('v1/', ChatBotView.as_view(), name='chatbot'),
]
