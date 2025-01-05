from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

from .models import User, OneTimePassword


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
