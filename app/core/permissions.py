"""
    Esse arquivo foi criado apenas como o intuito de iniciar o banco de dados com os
    grupos corretos e as permissões descritas no core.admin
    
    Note que ainda não pensei na melhor maneira de aplicar essas configurações levando
    em consideração que, esse arquivo só pode ser adcionado à lógica da aplicação após
    a migrate estar completa pois se não gera um erro por tentar criar antes das tabelas
    existirem. 
    
    Por agora, após fazer as migrações, insira no inicio do arquivo core.admin:
    
        From .permissions import PermissaoMixin
    
    E faça a seguinte alteração
    
        class PessoaAdmin(admin.ModelAdmin, PermissaoMixin):
    
    
"""
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from .models import IgrejaCasa, Pessoa


class PermissaoMixin:
    ## Criação dos grupos 
    discipulo = Group.objects.get_or_create(name = 'Discipulo')
    auxiliar_diacono = Group.objects.get_or_create(name = 'Auxiliar diácono')
    lider_g_caseiro = Group.objects.get_or_create(name = 'Lider do gurpo caseiro')
    diacono_bloco = Group.objects.get_or_create(name = 'Diácono bloco')
    diacono_geral = Group.objects.get_or_create(name = 'Diácono geral')
    presbitero = Group.objects.get_or_create(name = 'Presbítero')
    Administrador = Group.objects.get_or_create(name = 'Administrador')

    ## Criação das permissões para o model Pessoa
    ct = ContentType.objects.get_for_model(Pessoa)
    permission = Permission.objects.get_or_create(codename = 'pode_ver_editar_proprios_dado',
                                        name = 'Pode ver e editar os próprios dados',
                                        content_type = ct)
    permission = Permission.objects.get_or_create(codename = 'pode_ver_editar_grupo_caseiro',
                                        name = 'Pode ver e editar os díscipulos do seu grupo caseiro',
                                        content_type = ct)
    permission = Permission.objects.get_or_create(codename = 'pode_ver_grupo_caseiro',
                                        name = 'Pode ver os díscipulos do seu grupo caseiro',
                                        content_type = ct)
    permission = Permission.objects.get_or_create(codename = 'pode_ver_editar_proprio_bloco',
                                        name = 'Pode ver e editar os díscipulos e grupo caseiro do seu bloco',
                                        content_type = ct)
    permission = Permission.objects.get_or_create(codename = 'pode_ver_dados_toda_igreja',
                                        name = 'Pode ver todos os dados dos discípulos e grupo caseiro de toda igreja',
                                        content_type = ct)

    ## Criação das permissões para o model IgrejaCasa
    ct = ContentType.objects.get_for_model(IgrejaCasa)
    permission = Permission.objects.get_or_create(codename = 'pode_editar_tabela_grupo_caseiro',
                                        name = 'Pode ver e editar os díscipulos do seu grupo caseiro',
                                        content_type = ct)

  
