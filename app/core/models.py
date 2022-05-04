from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from app.core.manager import PessoaManager
from django.db import models

# Aqui você vai criar todos os models baseado em https://dbdiagram.io/d/620ac9c585022f4ee5924b0a


class MotivoAfastmento(models.Model):
    nome = models.CharField(
        'Descrição do motivo de afastamento', max_length=256)

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        verbose_name = 'Motivo do afastmento'
        verbose_name_plural = 'Motivos dos afastamentos'


class OrigemDiscipulo(models.Model):
    nome = models.CharField(
        'Origem do discípulo', max_length=256)

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        verbose_name = 'Origem do discípulo'
        verbose_name = 'Origens dos discípulos'


class Profissao(models.Model):
    nome = models.CharField(
        'Profissão', max_length=256)

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        verbose_name = 'Profissão'
        verbose_name_plural = 'Profissões'


class EstadoCivil(models.Model):
    nome = models.CharField(
        'Estado civil', max_length=256)

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        verbose_name = 'estado civil'
        verbose_name_plural = 'estados civis'


class Bloco(models.Model):
    nome = models.CharField(
        'Bloco', max_length=256)

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        verbose_name = 'Bloco'


class IgrejaCasa(models.Model):
    nome = models.CharField(
        'Grupo Caseiro', max_length=256)
    bloco = models.ForeignKey('Bloco', related_name='igreja_casa', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        verbose_name='Grupo caseiro'
        verbose_name_plural ='Grupos caseiros'


class Localidade(models.Model):
    nome=models.CharField(
        'Descrição do local', max_length = 256)

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        verbose_name='Localidade'


class Funcao(models.Model):
    nome=models.CharField(
        'Descrição da função', max_length = 256)

    def __str__(self):
        return f"{self.nome}"
    
    class Meta:
        verbose_name='Função'
        verbose_name_plural='Funções'


class NivelServico(models.Model):
    nome=models.CharField(
        'Decrição do nivel do serviço', max_length = 256)

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        verbose_name='Nível do serviço'
        verbose_name_plural='Niveis dos serviços'

class Pessoa(AbstractBaseUser, PermissionsMixin):
    pass
    SEXO_CHOICES = (
        ("F", "Feminino"),
        ("M", "Masculino"),
        ("N", "Nenhuma das opções")
    )
    
    email=models.EmailField('Endereço de email', unique=True)
    nome=models.CharField(max_length = 256)
    data_nascimento=models.DateField(
        'Data  nascimento')
    #########################################################
    discipulo_vinculado=models.BooleanField(
        'Está vinculado?', default=1)
    apelido=models.CharField(
        'Apelido', max_length = 256, blank = True)
    data_vinculacao_igreja_local=models.DateField(
        'Qual a data de vinculação?', null=True, blank = True)
    data_afastamento=models.DateField(null=True, blank = True)

    sexo=models.CharField(max_length=1, choices=SEXO_CHOICES, blank=True, null=True)
    #########################################

    # Esseas abaixo não devem ser editados
    is_staff=models.BooleanField('É da equipe?', default = False)
    is_active=models.BooleanField('Está ativo?', default = True)
    created_at=models.DateTimeField('Data de Cadastro', auto_now_add = True)

    '''
    ===============
    Relacionamentos
    ===============
    '''
    funcao=models.ForeignKey('Funcao', related_name = 'funcao', on_delete = models.CASCADE, null=True, blank=True)
    estado_civil=models.ForeignKey('EstadoCivil', related_name = 'estado_civil', on_delete = models.CASCADE, null=True, blank=True)
    igreja_casa=models.ForeignKey('IgrejaCasa', related_name = 'igreja_casa', on_delete = models.CASCADE, null=True, blank=True)
    localidade=models.ForeignKey('Localidade', related_name = 'localidade', on_delete = models.CASCADE, null=True, blank=True)
    nivel=models.ForeignKey('NivelServico', related_name = 'nivel', on_delete = models.CASCADE, null=True, blank=True)
    motivo_afastamento=models.ForeignKey('MotivoAfastmento', related_name = 'motivo_afastamento', on_delete = models.CASCADE, null=True, blank=True)
    origem=models.ForeignKey('OrigemDiscipulo', related_name = 'origem', on_delete = models.CASCADE, null=True, blank=True)
    profissao=models.ForeignKey('Profissao', related_name = 'profissão', on_delete = models.CASCADE, null=True, blank=True)
    pai=models.ForeignKey('self', related_name = 'pessoa_pai', on_delete = models.CASCADE, null=True, blank=True)
    mae=models.ForeignKey('self', related_name = 'pessoa_mae', on_delete = models.CASCADE, null=True, blank=True)
    ##########################################


    EMAIL_FIELD='email'
    USERNAME_FIELD='email'
    #REQUIRED_FIELDS=['email']

    objects=PessoaManager()

    def __str__(self):
        return f'{self.nome} - {self.data_nascimento}'

    class Meta:
        verbose_name='Pessoa'
        unique_together=('nome', 'data_nascimento')


class Permissao(models.Model):
    nome=models.CharField('Permissão', max_length = 256)
    descricao=models.CharField('Descrição da permissão', max_length = 256)

    def __str__(self):
        return f'{self.nome}'
    class Meta:
        verbose_name='Permissão'
        verbose_name_plural='Permissões'


class PessoaPermissao(models.Model):
    pessoa=models.ForeignKey('Pessoa', related_name = 'pessoas',
                                on_delete = models.CASCADE, blank=True, null=True)
    permissao=models.ForeignKey('Pessoa', related_name = 'permissao',
                                   on_delete = models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name='Permissão da pessoa'
        verbose_name_plural='Permissões das pessoas'
        unique_together=('pessoa', 'permissao')


class Conjugue(models.Model):
    marido=models.OneToOneField('Pessoa', related_name = 'marido',
                                on_delete = models.CASCADE)
    esposa=models.OneToOneField('Pessoa', related_name = 'esposa',
                                on_delete = models.CASCADE)

    class Meta:
        verbose_name='Cônjugue'


class JuntaCompanheirismo(models.Model):
    discipulo_um=models.ManyToManyField('Pessoa', related_name='discipulo_um')
    discipulo_dois=models.ManyToManyField('Pessoa', related_name='discipulo_dois')
    class Meta:
        verbose_name='Companheirismo'
        #unique_together=('discipulo_um', 'discipulo_dois')


class JuntaDiscipulado(models.Model):
    discipulador=models.ForeignKey('Pessoa', related_name='discipulador', on_delete= models.CASCADE)
    discipulo=models.ForeignKey('Pessoa', related_name='discipulo', on_delete= models.CASCADE)



    class Meta:
        verbose_name='Discipulado'
        unique_together=('discipulador', 'discipulo')


class Telefone(models.Model):
    numero=models.CharField('Telefone', max_length = 256)
    descricao=models.CharField('Descrição do telefone', max_length = 256)
    pessoa=models.ForeignKey(
        'Pessoa', related_name = 'telefones', on_delete = models.CASCADE)


    class Meta:
        verbose_name='Telefone'
