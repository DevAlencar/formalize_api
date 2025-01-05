import random
from django.core.mail import EmailMessage
import pyotp

from .models import User, OneTimePassword
from formalize_api import settings


def generate_otp():
    secret = pyotp.random_base32()
    otp = pyotp.TOTP(secret, interval=300)
    return secret, otp.now()


def send_otp(email):
    subject = "One time passcode Email verification"
    otp_secret, otp_code = generate_otp()
    user = User.objects.get(email=email)
    email_body = f"Hi {user.first_name}, thanks for signing up on Formalize.CA, your passcode is {otp_code} and is valid for 5 minutes"
    from_email = settings.DEFAULT_FROM_EMAIL

    OneTimePassword.objects.create(user = user, code = otp_code)
    user.otp_secret = otp_secret
    user.save()

    print(otp_secret)
    print(otp_code)

    send_email = EmailMessage(subject=subject, body=email_body, from_email=from_email, to=[email])
    send_email.send(fail_silently=True)


def send_normal_email(data):
    send_email = EmailMessage(subject=data['subject'], body=data['email_body'], from_email=settings.EMAIL_HOST_USER, to=[data['to_email']])
    send_email.send()