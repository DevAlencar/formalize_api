from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from .managers import UserManager


class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, verbose_name=_('Email Address'))
    otp_secret = models.CharField(max_length=32, unique=True, verbose_name=_('OTP Secret'), default=None, null=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True, verbose_name=_('CPF'), default=None) #todo verificação de CPF
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'cpf']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class OneTimePassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return self.user.first_name