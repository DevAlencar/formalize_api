from base64 import urlsafe_b64decode
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import pyotp
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import OneTimePassword, User
from .serializers import UserRegisterSerializer, OTPVerifySerializer, OTPResendSerializer, LoginSerializer, \
    PasswordResetRequestSerializer, SetNewPasswordSerializer, LogoutUserSerializer
from .utils import send_otp


class RegisterUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            send_otp(user['email'])
            return Response({'data': user,
                             'message': 'User created successfully!'},
                            status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendOTPView(GenericAPIView):
    serializer_class = OTPResendSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data['email'])
            otp_obj = send_otp(user.email)
            return Response({'message': 'OTP has been resent successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(GenericAPIView):
    serializer_class = OTPVerifySerializer

    def post(self, request):
        otp_code = request.data.get('otp')

        try:
            otp_obj = OneTimePassword.objects.get(code=otp_code)
            user = otp_obj.user

            totp = pyotp.TOTP(user.otp_secret, interval=300)
            if totp.verify(otp_code):
                if not user.is_verified:
                    user.is_verified = True
                    user.save()
                    return Response({'message': 'User verified!'},
                                    status=status.HTTP_200_OK)
                return Response({'message': 'User is already verified!'},
                                status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'Invalid token!'},
                                status=status.HTTP_400_BAD_REQUEST)

        except OneTimePassword.DoesNotExist:
            return Response({'message': 'Invalid token!'},
                            status=status.HTTP_404_NOT_FOUND)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'message':'A link has been sent to your email'}, status=status.HTTP_200_OK)


class PasswordResetConfirm(GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            padded_uidb64 = uidb64 + '=' * ((4 - len(uidb64) % 4) % 4)
            user_id = smart_str(urlsafe_b64decode(padded_uidb64))
            user = User.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'message': 'Invalid token!'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'success': True, 'uidb64': uidb64, 'token':token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError:
            return Response({'message': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    def patch(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'New password has been set.'}, status=status.HTTP_200_OK)


class LogoutUserView(GenericAPIView):
    serializer_class = LogoutUserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'User has been logged out.'}, status=status.HTTP_204_NO_CONTENT)