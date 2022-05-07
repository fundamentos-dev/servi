"""
    Esse arquivo foi criado apenas como o intuito de iniciar o banco de dados com os
    grupos corretos e as permissões descritas no core.admin
    
    Após fazer a migração do banco de dados rode a class 
    'PermissaoMixin' no terminal.
    
"""
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from .models import GrupoCaseiro, Pessoa


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
    permission = Permission.objects.get_or_create(codename = 'pode_ver_editar_proprios_dados',
                                        name = 'Pode ver e editar os próprios dados',
                                        content_type = ct)
    permission = Permission.objects.get_or_create(codename = 'pode_ver_editar_discipulos_grupo_caseiro',
                                        name = 'Pode ver e editar os díscipulos do seu grupo caseiro',
                                        content_type = ct)
    permission = Permission.objects.get_or_create(codename = 'pode_ver_discipulos_grupo_caseiro',
                                        name = 'Pode ver os díscipulos do seu grupo caseiro',
                                        content_type = ct)
    permission = Permission.objects.get_or_create(codename = 'pode_ver_editar_proprio_bloco',
                                        name = 'Pode ver e editar os díscipulos e grupo caseiro do seu bloco',
                                        content_type = ct)
    permission = Permission.objects.get_or_create(codename = 'pode_ver_dados_toda_igreja',
                                        name = 'Pode ver todos os dados dos discípulos e grupo caseiro de toda igreja',
                                        content_type = ct)

    ## Criação das permissões para o model GrupoCaseiro
    ct = ContentType.objects.get_for_model(GrupoCaseiro)
    permission = Permission.objects.get_or_create(codename = 'pode_editar_tabela_grupo_caseiro',
                                        name = 'Pode ver e editar os díscipulos do seu grupo caseiro',
                                        content_type = ct)

  
