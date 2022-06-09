from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
import random
import string
import datetime

class PessoaManager(BaseUserManager):
    """
    Custom user model manager 
    """

    def create_user(self, nome, password=None, username=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        print('Creating user...')

        if not username:
            # generate username
            username = nome.lower().replace(' ', '')[:16]
        if not password:
            # generate random password
            password = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
            # send email if there is an email with random pass

        user = self.model(nome=nome, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, nome, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        date = datetime.date(1995, 11, 1)
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('data_nascimento', date)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(nome, password, **extra_fields)
