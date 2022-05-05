from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from app.core.manager import PessoaManager
from django.db import models

# Aqui você vai criar todos os models baseado em https://dbdiagram.io/d/620ac9c585022f4ee5924b0a
class MotivoAfastmento(models.Model):
    # TODO deve ser colocado também aqui o nome verboso de cada coluna, já qu eiremos utilizar bastante o painel admin é importante que esteja compreensível
    nome = models.CharField(
        'Descrição do motivo de afastamento', max_length=256)

    def __str__(self):
        return f"{self.nome}"
    
    class Meta:
        # TODO verbose name sempre deve ser algo pensado no usuário, uma frase em CammelCase não é algo visivel e atrativo ao usuário
        verbose_name = 'Motivo do afastmento'
        verbose_name_plural = 'Motivos dos afastamentos'


class OrigemDiscipulo(models.Model):
    # TODO por default os campos já vem como obrigatórios, dessa forma não é necessário o blank=False e o null=False
    nome = models.CharField(
        'Origem do discípulo', max_length=256)

    def __str__(self):
        return f"{self.nome}"
    
    class Meta:
        verbose_name = 'OrigemDiscipulo'


class Profissao(models.Model):
    nome = models.CharField(max_length=256, blank=False, null=False)

    def __str__(self):
        return f"{self.nome}"
    
    class Meta:
        # TODO No verbose name pode e devem ser usados acentos, para inteligibilidade do usuário
        verbose_name = 'Profissão'
        verbose_name_plural = 'Profissões'


class EstadoCivil(models.Model):
    nome = models.CharField(max_length=256, blank=False, null=False)

    def __str__(self):
        return f"{self.nome}"
    
    class Meta:
        verbose_name = 'EstadoCivil'


class Bloco(models.Model):
    nome = models.CharField(max_length=256, blank=False, null=False)

    def __str__(self):
        return f"{self.nome}"
    
    class Meta:
        verbose_name = 'Bloco'


class IgrejaCasa(models.Model):
    nome = models.CharField(max_length=256, blank=False, null=False)
    bloco_id = models.ForeignKey('Bloco', related_name='igreja_casa', on_delete=models.CASCADE, null=False, blank=False),

    def __str__(self):
        return f"{self.nome}"
    
    class Meta:
        verbose_name = 'IgrejaCasa'


class Localidade(models.Model):
    nome = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.nome}"
    
    class Meta:
        verbose_name = 'Localidade'


class Funcao(models.Model):
    nome = models.CharField(max_length=256, null=False, blank=False)

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        verbose_name = 'Funcao'


class NivelServico(models.Model):
    nome = models.CharField(max_length=256, blank=False, null=False)

    def __str__(self):
        return f"{self.nome}"
    
    class Meta:
        verbose_name='Nível do serviço'
        verbose_name='Niveis dos serviços'

class Pessoa(AbstractBaseUser, PermissionsMixin):
    SEXO_CHOICES = (
        ("F", "Feminino"),
        ("M", "Masculino"),
        ("N", "Nenhuma das opções")
    )
    email = models.EmailField('Endereço de email')
    nome = models.CharField(max_length=256, null=False, blank=False)
    data_nascimento = models.DateField('Data de nascimento', null=False, blank=False)
    #########################################################
    discipulo_vinculado=models.BooleanField(
        'Está vinculado?', default=1)
    apelido=models.CharField(
        'Apelido', max_length = 256, blank = True)
    data_vinculacao_igreja_local=models.DateField(
        'Qual a data de vinculação?', null=True, blank = True)
    data_afastamento=models.DateField(null=True, blank = True)
    # ! Não entendi o pq desse length em sexo, estava assim lá?
    sexo=models.CharField(max_length=1, choices=SEXO_CHOICES, blank=True, null=True)
    #########################################
    
    # Esseas abaixo não devem ser editados
    is_staff = models.BooleanField('Está ativo?', default=False)
    is_active = models.BooleanField('É da equipe?', default=True)
    created_at = models.DateTimeField('Data de Cadastro', auto_now_add=True)

    '''
    ===============
    Relacionamentos
    ===============
    '''
    # TODO Novamente reforçando sobre a legibilidade dos verbose names
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

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = PessoaManager()
    
    def __str__(self):
        return f'{self.nome} - {self.data_nascimento}'

    class Meta:
        verbose_name = 'Pessoa'
        unique_together = ('nome', 'data_nascimento')
        
        
class Permissao(models.Model):
    nome = models.CharField(max_length=256, blank=False, null=False)
    descricao = models.CharField(max_length=256, null=False, blank=False)

    def __str__(self):
        return f'{self.nome}
    class Meta:
        verbose_name = 'Permissao'


class PessoaPermissao(models.Model):
    pessoa_id = models.ForeignKey('Pessoa', related_name='pessoa_pessoas_permissao', on_delete=models.CASCADE, blank=False, null=False)
    permissao_id = models.ForeignKey('Pessoa', related_name='permicao_pessoas_permissao', on_delete=models.CASCADE, blank=False, null=False)

    ## Precisa retonar str? 
    class Meta:
        verbose_name = 'PessoaPermissao'


class Conjugue(models.Model):
    marido_id = models.ForeignKey('Pessoa', related_name='marido_conjugues', on_delete=models.CASCADE, blank=False, null=False)
    esposa_id = models.ForeignKey('Pessoa', related_name='esposa_conjugues', on_delete=models.CASCADE, blank=False, null=False)

    ## Precisa retonar str?
    class Meta:
        verbose_name = 'Telefone' 


class JuntaCompanheirismo(models.Model):
    discipulo_um_id = models.CharField(max_length=50, blank=True)
    discipulo_dois_id = models.CharField(max_length=50, blank=True)

    ## Precisa retonar str? 
    class Meta:
        verbose_name = 'JuntaCompanheirismo'
        unique_together = ('discipulo_um_id', 'discipulo_dois_id')


class JuntaDiscipulado(models.Model):
    discipulador_id = models.CharField(max_length=50, blank=True)
    discipulo_id = models.CharField(max_length=50, blank=True)

    ## Precisa retonar str? 
    class Meta:
        verbose_name = 'JuntaDiscipulado'
        unique_together = ('discipulador_id', 'discipulo_id')


class Telefone(models.Model):
    numero = models.CharField(max_length=256, null=False, blank=False)
    descricao = models.CharField(max_length=256, null=False, blank=False)
    pessoa = models.ForeignKey(
        'Pessoa', related_name='telefones', on_delete=models.CASCADE)

    ## Precisa retonar str? 
    class Meta:
        verbose_name = 'Telefone'