"""
    Esse arquivo foi criado apenas como o intuito de iniciar o banco de dados com os
    grupos corretos e as permissões descritas no core.admin
    
    Após fazer a migração do banco de dados rode a class 
    'PermissaoMixin' no terminal.
    
"""
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from .models import GrupoCaseiro, Pessoa, Bloco


class PermissaoMixin:
    ## Criação dos grupos 
    discipulo = Group.objects.get_or_create(name = 'Discipulo')
    lider_g_caseiro = Group.objects.get_or_create(name = 'Lider do gurpo caseiro')
    auxiliar_diacono = Group.objects.get_or_create(name = 'Auxiliar diácono')
    diacono_bloco = Group.objects.get_or_create(name = 'Diácono bloco')
    diacono_geral = Group.objects.get_or_create(name = 'Diácono geral')
    presbitero = Group.objects.get_or_create(name = 'Presbítero')
    Administrador = Group.objects.get_or_create(name = 'Administrador')
    
    ## Criação dos ContentTypes que estão sendo utilizados
    ct_pessoa = ContentType.objects.get_for_model(Pessoa)
    ct_grupo_caseiro = ContentType.objects.get_for_model(GrupoCaseiro)
    
    ## Criação das permissões para o model Pessoa
    permission_discipulo = Permission.objects.get_or_create(codename = 'pode_ver_editar_proprios_dados',
                                        name = 'Pode ver e editar os próprios dados',
                                        content_type = ct_pessoa)
    permission_auxiliar_diacono = Permission.objects.get_or_create(codename = 'pode_ver_editar_discipulos_grupo_caseiro',
                                        name = 'Pode ver e editar os díscipulos do seu grupo caseiro',
                                        content_type = ct_pessoa)
    permission_lider_g_caseiro= Permission.objects.get_or_create(codename = 'pode_ver_discipulos_grupo_caseiro',
                                        name = 'Pode ver os díscipulos do seu grupo caseiro',
                                        content_type = ct_pessoa)
    permission_diacono_bloco = Permission.objects.get_or_create(codename = 'pode_ver_editar_proprio_bloco',
                                        name = 'Pode ver e editar os díscipulos e grupo caseiro do seu bloco',
                                        content_type = ct_pessoa)
    permission_diacono_geral = Permission.objects.get_or_create(codename = 'pode_ver__editar_dados_toda_igreja',
                                        name = 'Pode ver e editar todos os dados dos discípulos e grupo caseiro de toda igreja',
                                        content_type = ct_pessoa)
    permission_presbitero = Permission.objects.get_or_create(codename = 'pode_ver_dados_toda_igreja',
                                        name = 'Pode ver todos os dados dos discípulos e grupo caseiro de toda igreja',
                                        content_type = ct_pessoa)

    ## Criação das permissões para o model GrupoCaseiro
    permission_diaconos = Permission.objects.get_or_create(codename = 'pode_ver_editar_tabela_grupo_caseiro',
                                        name = 'Pode ver e editar os díscipulos do seu grupo caseiro',
                                        content_type = ct_grupo_caseiro)
    
    # Associando grupos às permissões
    discipulo.permissions.add(permission_discipulo)
    auxiliar_diacono.permissions.add(permission_auxiliar_diacono)
    lider_g_caseiro.permissions.add(permission_lider_g_caseiro)
    diacono_bloco.permissions.add(permission_diacono_bloco)
    diacono_bloco.permissions.add(permission_diaconos)
    diacono_geral.permissions.add(permission_diacono_geral)
    diacono_geral.permissions.add(permission_diaconos)
    presbitero.permissions.add(permission_presbitero)
  
