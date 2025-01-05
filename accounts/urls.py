from django.urls import path

from .views import RegisterUserView, VerifyEmailView, ResendOTPView, LoginView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('otp_resend/', ResendOTPView.as_view(), name='otp_resend'),
    path('verify/', VerifyEmailView.as_view(), name='verify'),
    path('login/', LoginView.as_view(), name='login'),
]