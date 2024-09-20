from django.urls import path
from .views import ChatbotView

urlpatterns = [
    path('v1/', ChatbotView.as_view(), name='chatbot'),
]
