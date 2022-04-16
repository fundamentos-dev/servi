from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from app.core.manager import PessoaManager
from django.db import models

# Aqui você vai criar todos os models baseado em https://dbdiagram.io/d/620ac9c585022f4ee5924b0a

class Pessoa(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Endereço de email')
    nome = models.CharField(max_length=256, null=False, blank=False)
    data_nascimento = models.DateField('Data de nascimento', null=False, blank=False)
    discipulo_vinculado = models.DateField('Data de nascimento', null=False, blank=False)
    
    # Esseas abaixo não devem ser editados
    is_staff = models.BooleanField('Está ativo?', default=False)
    is_active = models.BooleanField('É da equipe?', default=True)
    created_at = models.DateTimeField('Data de Cadastro', auto_now_add=True)

    # Relacionamentos
    funcao = models.ForeignKey(
        'Funcao', related_name='pessoas', on_delete=models.CASCADE)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = PessoaManager()

    def __str__(self):
        return f'{self.nome} - {self.data_nascimento}'

    class Meta:
        verbose_name = 'Pessoa'

class Funcao(models.Model):
    nome = models.CharField(max_length=256, null=False, blank=False)

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        verbose_name = 'Funcao'

class Telefone(models.Model):
    numero = models.CharField(max_length=256, null=False, blank=False)
    descricao = models.CharField(max_length=256, null=False, blank=False)
    pessoa = models.ForeignKey(
        'Pessoa', related_name='telefones', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        verbose_name = 'Funcao'