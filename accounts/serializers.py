from tokenize import TokenError

from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_str, smart_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken, Token

from .models import User, OneTimePassword
from .utils import send_normal_email


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'cpf', 'first_name', 'last_name', 'password', 'password2']


    def validate(self, attrs):
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')
        if password != password2:
            raise serializers.ValidationError('Passwords must match')
        return attrs


    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            cpf=validated_data['cpf'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
        )

        return user


class OTPResendSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()
        if not user or user.is_verified:
            raise serializers.ValidationError("No user found with this email or user ir already verified.")
        return value


class OTPVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(required=True, max_length=6, min_length=6, help_text="OTP code from your email")

    def validate_otp(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Invalid OTP format.")
        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=6, help_text="Email address")
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    full_name = serializers.CharField(max_length=255, read_only=True, help_text="Full name")
    access_token = serializers.CharField(max_length=255, read_only=True, help_text="Access token")
    refresh_token = serializers.CharField(max_length=255, read_only=True, help_text="Refresh token")

    class Meta:
        model = User
        fields = ['email', 'password', 'full_name', 'access_token', 'refresh_token']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request, email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        user_tokens = user.tokens()

        return {
            'email': user.email,
            'full_name': user.get_full_name,
            'access_token': str(user_tokens.get('access')),
            'refresh_token': str(user_tokens.get('refresh')),
        }


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=6, help_text="Email address")

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            request = self.context.get('request')
            site_domain = get_current_site(request).domain
            relative_link = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            abslink = f"http://{site_domain}{relative_link}"
            email_body = f"Use the link bellow to reset your password: \n {abslink}"
            data = {
                'email_body': email_body,
                'subject': 'Password Reset Request',
                'to_email': user.email,
            }
            send_normal_email(data)

        return super().validate(attrs)


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    confirm_password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    class Meta:
        fields = ['password', 'confirm_password', 'uidb64', 'token']

    def validate(self, attrs):
        try:
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')

            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('Invalid token')
            if password != confirm_password:
                raise AuthenticationFailed('Passwords do not match')
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            raise AuthenticationFailed(e)


class LogoutUserSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    default_error_message = {
        'bad_token': 'Invalid token',
    }

    def validate(self, attrs):
        self.token = attrs.get('refresh_token')
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad token')