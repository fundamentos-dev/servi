from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from unidecode import unidecode
from django.core.mail import send_mail

import os
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
        print('Criando usuário...')
        print(nome, password, username, extra_fields)

        if not username:
            # generate username
            username = unidecode(nome).replace(" ", "").lower()[:8]
            # Verifica se já existe esse username
            count = len(self.model.objects.filter(username=username).all())
            if count > 0:
                # Tenta adicionar os últimos caracteres da data de nascimento
                username = f"{username}{extra_fields['data_nascimento'].strftime('%Y')[2:4]}"
                # Usa números aleatórios até encontrar um
                while len(self.model.objects.filter(username=username).all()) > 0:
                    username = f'{username}{random.randint(0, 99)}'
                    

        if not password:
            # generate random password
            password = ''.join(random.choice(string.ascii_lowercase) for i in range(8))

        # send email if there is an email with random pass
        print(f'Senha criada para {username} é {password}')
        if extra_fields['email']:
            send_mail(
                subject='Você acabou de ser cadastrado!',
                message=f'Você acabou de ser cadastrado no Cadastro Geral de Discípulos (CGD) da Igreja em Salvador. Pode acessar o seu cadastro e editá-lo pelo link: https://cgd.igrejaemsalvador.org. Seu usuário de acesso é {username} e sua senha de acesso é {password}'
                html_message=f'''
                <p>olá {nome},</p>
                <p>Você acabou de ser cadastrado no Cadastro Geral de Discípulos (CGD) da Igreja em Salvador. Pode acessar o seu cadastro e editá-lo <a href="https://cgd.igrejaemsalvador.org">nesse link</a>. Seu usuário de acesso é {username} e sua senha de acesso é <strong>{password}</strong></p>
                <p>Atenciosamente,</p>
                <p>Equipe de Diaconato da Igreja em Salvador</p>
                ''',
                from_email=os.environ.get('EMAIL_USER'),
                recipient_list=[extra_fields['email']],
                fail_silently=False,
            )

        # Envia email para o próprio email do cadastro para informar que houve cadastro
        send_mail(
            subject=f'Novo cadastro de discípulo - {nome}',
            message=f'usuário criado. Nome: {nome}, usuário: {username}, senha: {password}'
            html_message=f'''
            <p>Um discípulo acabou de ser cadastrado:<p>
            <p>
            Nome: <strong>{nome}</strong><br/>
            Usuário: <strong>{username}</strong><br/>
            Senha: <strong>{password}</strong><br/>
            </p>''',
            from_email=os.environ.get('EMAIL_USER'),
            recipient_list=[os.environ.get('EMAIL_USER')],
            fail_silently=False,
        )

        user = self.model(nome=nome, username=username, **extra_fields)
        user.set_password(password)
        user.save()

        print(f'Usuário criado')
        return user

    def create_superuser(self, nome, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        print('Criando superuser...')

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
