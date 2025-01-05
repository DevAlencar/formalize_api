from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
import re


class UserManager(BaseUserManager):
    def cpf_validator(self, cpf):
        cpf = re.sub(r'\D', '', cpf)

        if len(cpf) != 11 or cpf in ["00000000000", "11111111111", "22222222222", "33333333333", "44444444444",
                                     "55555555555", "66666666666", "77777777777", "88888888888", "99999999999"]:
            return False

        try:
            digito_1 = 0
            digito_2 = 0

            for i in range(9):
                digito_1 += int(cpf[i]) * (10 - i)
                digito_2 += int(cpf[i]) * (11 - i)

            digito_1 = 11 - (digito_1 % 11)
            if digito_1 >= 10:
                digito_1 = 0

            digito_2 += digito_1 * 2
            digito_2 = 11 - (digito_2 % 11)
            if digito_2 >= 10:
                digito_2 = 0

            return cpf[-2:] == f"{digito_1}{digito_2}"

        except ValueError:
            return False

    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("Email address is invalid."))

    def create_user(self, email, password, first_name, last_name, cpf, **extra_fields):
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("Email adress is required."))
        if not self.cpf_validator(cpf):
                raise ValueError(_("CPF is invalid."))
        if not first_name:
            raise ValueError(_("First name is required."))
        if not last_name:
            raise ValueError(_("Last name is required."))
        user = self.model(email=email, cpf=cpf, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.username = email
        user.save(using=self._db)
        return user

    def create_superuser(self, email, cpf, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        user = self.create_user(email, password, first_name, last_name, cpf, **extra_fields)
        user.save(using=self._db)
        return user