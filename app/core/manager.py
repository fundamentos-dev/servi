from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _


class PessoaManager(BaseUserManager):
    """
    Custom user model manager 
    """

    def save_model(self, *args, **kwargs):
        g_lider_caseiro = Group.objects.get(name='Lider do gurpo caseiro')
        g_presbitero = Group.objects.get(name='Presbítero')
        g_discipulo = Group.objects.get(name='Discípulo')
        print('Saveeeee')
        if not self.pk:
            raise ValueError(_('error'))
        if self.nivel_servico.nome == 'Líder do grupo caseiro':
            print('ENTROUUUU')
            g_lider_caseiro.user_set.add(self.pk)
        elif self.nivel_servico.id == 8:
            g_presbitero.user_set.add(self.pk)
        print("Sendo salvo pela primeira vez")
        super().save(*args, **kwargs)

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
