# Adicionando usuários de teste
from django.contrib.auth import get_user_model
import datetime
# Criando Igreja na casa de Teste
# Criando Bloco de teste
# Criando Pessoas de teste com permissões
birthdate = datetime.date(1995,11,1)
User = get_user_model()
User(nome="Presbítero de Teste", email="presbitero@teste.br", data_nascimento=birthdate, is_staff=True).save()
User(nome="Diácono Local de Teste", email="diaconolocal@teste.br", data_nascimento=birthdate, is_staff=True).save()
User(nome="Diácono Local de Teste", email="diaconogeral@teste.br", data_nascimento=birthdate, is_staff=True).save()
colaborador = User.objects.get(username="colaborador")
colaborador.set_password("passw@rd")

from app.core import models
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

discipulo, created = Group.objects.get_or_create(name = 'Discípulo')
lider_g_caseiro, created = Group.objects.get_or_create(name = 'Lider do gurpo caseiro')
auxiliar_diacono, created = Group.objects.get_or_create(name = 'Auxiliar diácono')
diacono_bloco, created = Group.objects.get_or_create(name = 'Diácono bloco')
diacono_geral, created = Group.objects.get_or_create(name = 'Diácono geral')
presbitero, created = Group.objects.get_or_create(name = 'Presbítero')
administrador, created = Group.objects.get_or_create(name = 'Administrador')

## Criação dos ContentTypes que estão sendo utilizados
ct_pessoa = ContentType.objects.get_for_model(models.Pessoa)
ct_grupo_caseiro = ContentType.objects.get_for_model(models.GrupoCaseiro)
ct_motivo_afastamento = ContentType.objects.get_for_model(models.MotivoAfastamento)
ct_origem_discipulo = ContentType.objects.get_for_model(models.OrigemDiscipulo)
ct_profissao = ContentType.objects.get_for_model(models.Profissao)
ct_estado_civil = ContentType.objects.get_for_model(models.EstadoCivil)
ct_bloco = ContentType.objects.get_for_model(models.Bloco)
ct_localidade = ContentType.objects.get_for_model(models.Localidade)
ct_funcao = ContentType.objects.get_for_model(models.Funcao)
ct_nivel_servico = ContentType.objects.get_for_model(models.NivelServico)
ct_permissao = ContentType.objects.get_for_model(models.Permissao)
ct_pessoa_permissao = ContentType.objects.get_for_model(models.PessoaPermissao)
ct_conjugue = ContentType.objects.get_for_model(models.Conjugue)
ct_junta_discipulado = ContentType.objects.get_for_model(models.JuntaDiscipulado)
ct_telefone = ContentType.objects.get_for_model(models.Telefone)


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


## Criação das permissões para o model MotivoAfastamento
permission_motivo_afastamento = Permission.objects.get_or_create(codename = 'pode_ver_editar_tabela_motivo_afastamento',
                                    name = 'Pode ver e editar a tabela motivo do afastamento',
                                    content_type = ct_motivo_afastamento)


## Criação das permissões para o model OrigemDiscipulo
permission_origem_discipulo = Permission.objects.get_or_create(codename = 'pode_ver_editar_tabela_origem_discipulo',
                                    name = 'Pode ver e editar a tabela origem do discípulo',
                                    content_type = ct_origem_discipulo)


## Criação das permissões para o model Profissao
permission_profissao = Permission.objects.get_or_create(codename = 'pode_ver_editar_tabela_profissao',
                                    name = 'Pode ver e editar a tabela profissão',
                                    content_type = ct_profissao)


## Criação das permissões para o model EstadoCivil
permission_estado_civil = Permission.objects.get_or_create(codename = 'pode_ver_editar_tabela_estado_civil',
                                    name = 'Pode ver e editar a tabela estado civil',
                                    content_type = ct_estado_civil)


## Criação das permissões para o model Bloco
permission_bloco = Permission.objects.get_or_create(codename = 'pode_ver_editar_tabela_bloco',
                                    name = 'Pode ver e editar a tabela bloco',
                                    content_type = ct_bloco)


## Criação das permissões para o model Localidade
permission_localidade = Permission.objects.get_or_create(codename = 'pode_ver_editar_tabela_localidade',
                                    name = 'Pode ver e editar a tabela localidade',
                                    content_type = ct_localidade)


## Criação das permissões para o model Funcao
permission_funcao = Permission.objects.get_or_create(codename = 'pode_ver_editar_tabela_funcao',
                                    name = 'Pode ver e editar a tabela função',
                                    content_type = ct_funcao)


## Criação das permissões para o model NivelServico
permission_nivel_servico = Permission.objects.get_or_create(codename = 'pode_ver_editar_tabela_nivel_servico',
                                    name = 'Pode ver e editar a tabela nível serviço',
                                    content_type = ct_nivel_servico)


## Criação das permissões para o model Permissao
permission_permissao = Permission.objects.get_or_create(codename = 'pode_ver_editar_tabela_permissao',
                                    name = 'Pode ver e editar a tabela permissão',
                                    content_type = ct_permissao)


## Criação das permissões para o model PessoaPermissao
permission_pessoa_permissao = Permission.objects.get_or_create(codename = 'pode_ver_editar_tabela_pessoa_permissao',
                                    name = 'Pode ver e editar a tabela pessoa permissão',
                                    content_type = ct_pessoa_permissao)


## Criação das permissões para o model Conjugue
permission_conjugue = Permission.objects.get_or_create(codename = 'pode_ver_editar_tabela_conjugue',
                                    name = 'Pode ver e editar a tabela conjugue',
                                    content_type = ct_conjugue)


## Criação das permissões para o model JuntaDiscipulado
permission_junta_discipulado = Permission.objects.get_or_create(codename = 'pode_ver_editar_tabela_junta_discipulado',
                                    name = 'Pode ver e editar a tabela junta discipulado',
                                    content_type = ct_junta_discipulado)


## Criação das permissões para o model Telefone
permission_telefone = Permission.objects.get_or_create(codename = 'pode_ver_editar_tabela_telefone',
                                    name = 'Pode ver e editar a tabela telefone',
                                    content_type = ct_telefone)



# # Associando grupos às permissões
# discipulo.permissions.add(permission_discipulo)
# auxiliar_diacono.permissions.add(permission_auxiliar_diacono)
# lider_g_caseiro.permissions.add(permission_lider_g_caseiro)
# diacono_bloco.permissions.add(permission_diacono_bloco,
#                                 permission_diacono_bloco_geral,
#                                 permission_diaconos)
# diacono_geral.permissions.add(permission_presbitero_diacono_geral,
#                                 permission_diacono_bloco_geral,
#                                 permission_diaconos)
# presbitero.permissions.add(permission_presbitero_diacono_geral)
