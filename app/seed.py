# Adicionando usuários de teste
from django.contrib.auth import get_user_model
import datetime
# Criando Igreja na casa de Teste
# Criando Bloco de teste
# Criando Pessoas de teste com permissões
birthdate = datetime.date(1995,11,1)
User = get_user_model()
User(name="Presbítero de Teste", email="presbitero@teste.br", data_nascimento=birthdate, is_staff=True).save()
User(name="Diácono Local de Teste", email="diaconolocal@teste.br", data_nascimento=birthdate, is_staff=True).save()
User(name="Diácono Local de Teste", email="diaconogeral@teste.br", data_nascimento=birthdate, is_staff=True).save()
colaborador = User.objects.get(username="colaborador")
colaborador.set_password("passw@rd")

from app.core.models import Bloco, GrupoCaseiro, Pessoa
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

discipulo, created = Group.objects.get_or_create(name = 'Discípulo')
lider_g_caseiro, created = Group.objects.get_or_create(name = 'Lider do gurpo caseiro')
auxiliar_diacono, created = Group.objects.get_or_create(name = 'Auxiliar diácono')
diacono_bloco, created = Group.objects.get_or_create(name = 'Diácono bloco')
diacono_geral, created = Group.objects.get_or_create(name = 'Diácono geral')
presbitero, created = Group.objects.get_or_create(name = 'Presbítero')
Administrador, created = Group.objects.get_or_create(name = 'Administrador')

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
permission_lider_g_caseiro = Permission.objects.get_or_create(codename = 'pode_ver_discipulos_grupo_caseiro',
                                    name = 'Pode ver os díscipulos do seu grupo caseiro',
                                    content_type = ct_pessoa)
permission_diacono_bloco = Permission.objects.get_or_create(codename = 'pode_ver_proprio_bloco',
                                    name = 'Pode ver os díscipulos e grupo caseiro do seu bloco',
                                    content_type = ct_pessoa)

permission_diacono_bloco_geral = Permission.objects.get_or_create(codename = 'pode_editar_proprio_bloco',
                                    name = 'Pode editar os díscipulos e grupo caseiro do seu bloco',
                                    content_type = ct_pessoa)

permission_presbitero_diacono_geral = Permission.objects.get_or_create(codename = 'pode_ver_dados_toda_igreja',
                                    name = 'Pode ver todos os dados dos discípulos e grupo caseiro de toda igreja',
                                    content_type = ct_pessoa)

## Criação das permissões para o model GrupoCaseiro
permission_diaconos = Permission.objects.get_or_create(codename = 'pode_ver_editar_tabela_grupo_caseiro',
                                    name = 'Pode ver e editar a tabela grupo caseiro',
                                    content_type = ct_grupo_caseiro)

# Associando grupos às permissões
discipulo.permissions.add(permission_discipulo)
auxiliar_diacono.permissions.add(permission_auxiliar_diacono)
lider_g_caseiro.permissions.add(permission_lider_g_caseiro)
diacono_bloco.permissions.add(permission_diacono_bloco,
                                permission_diacono_bloco_geral,
                                permission_diaconos)
diacono_geral.permissions.add(permission_presbitero_diacono_geral,
                                permission_diacono_bloco_geral,
                                permission_diaconos)
presbitero.permissions.add(permission_presbitero_diacono_geral)
