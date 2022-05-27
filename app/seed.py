# Adicionando usuários de teste
import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

from app.core import models
from app.core.models import Bloco, Funcao, GrupoCaseiro, NivelServico, EstadoCivil

# Selecionando Nível de Serviço
nivel_servico_lider = NivelServico.objects.get(id=6)
nivel_servico_presbitero = NivelServico.objects.get(id=8)

# Selecionando Função
funcao_auxiliar_diacono = Funcao.objects.get(id=1)
funcao_diacono_bloco = Funcao.objects.get(id=2)
funcao_diacono_geral = Funcao.objects.get(id=3)
funcao_presbitero = Funcao.objects.get(id=4)
funcao_administrador = Funcao.objects.get(id=5)

# Selecionando Estado Civil
estado_civil_solteiro = EstadoCivil.objects.get(id=1)
estado_civil_casado = EstadoCivil.objects.get(id=2)
estado_civil_divorciado = EstadoCivil.objects.get(id=3)




# Selecionando Bloco para teste
bloco = Bloco.objects.get(id=1)

# Criando Igreja na casa de Teste
grupo_caseiro, _ = GrupoCaseiro.objects.get_or_create(nome="Grupo Caseiro de Teste", bloco=bloco)

# Declarando variáveis de uso comum
date = datetime.date(1995, 11, 1)
User = get_user_model()

# Criando usuários de teste
presbitero, _ = User.objects.get_or_create(nome="Presbítero de Teste", email="presbitero@teste.br", data_nascimento=date, is_staff=True, is_active=True,
     grupo_caseiro=grupo_caseiro, nivel_servico=nivel_servico_presbitero, funcao=funcao_presbitero, estado_civil=estado_civil_solteiro, data_vinculacao_igreja_local=date)
diacono_bloco, _ = User.objects.get_or_create(nome="Diácono Local de Teste", email="diaconolocal@teste.br",
     data_nascimento=date, is_staff=True, is_active=True, funcao=funcao_diacono_bloco, estado_civil=estado_civil_casado, data_vinculacao_igreja_local=date)
diacono_geral, _ = User.objects.get_or_create(nome="Diácono Geral de Teste", email="diaconogeral@teste.br",
     data_nascimento=date, is_staff=True, is_active=True, funcao=funcao_diacono_geral, estado_civil=estado_civil_casado)
lider, _ = User.objects.get_or_create(nome="Líder de Teste", email="lider@teste.br", data_nascimento=date,
     is_staff=True, is_active=True, nivel_servico=nivel_servico_lider, estado_civil=estado_civil_solteiro, data_vinculacao_igreja_local=date)
discipulo, _ = User.objects.get_or_create(nome="Discípulo de Teste", email="discipulo@teste.br",
     data_nascimento=date, is_staff=True, is_active=True, estado_civil=estado_civil_casado)
auxiliar_diacono, _ = User.objects.get_or_create(nome="Auxiliar de Diácono de Teste", email="auxiliardiacono@teste.br",
     data_nascimento=date, is_staff=True, is_active=True, funcao=funcao_auxiliar_diacono, estado_civil=estado_civil_divorciado, data_vinculacao_igreja_local=date)
administrador, _ = User.objects.get_or_create(nome="Administrador", email="administrador@teste.br",
     data_nascimento=date, is_staff=True, is_active=True, funcao=funcao_administrador, estado_civil=estado_civil_divorciado)

# Atribuindo senha comum aos usuários de teste
presbitero.set_password("passw@rd")
diacono_bloco.set_password("passw@rd")
diacono_geral.set_password("passw@rd")
lider.set_password("passw@rd")
discipulo.set_password("passw@rd")
auxiliar_diacono.set_password("passw@rd")
administrador.set_password("passw@rd")

# Salvando alterações realizadas em usuário
presbitero.save()
diacono_bloco.save()
diacono_geral.save()
lider.save()
discipulo.save()
auxiliar_diacono.save()
administrador.save()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from app.core import models

## Criação dos grupos 
g_discipulo, _ = Group.objects.get_or_create(name = 'Discípulo')
g_lider_g_caseiro, _ = Group.objects.get_or_create(name = 'Lider do gurpo caseiro')
g_auxiliar_diacono, _ = Group.objects.get_or_create(name = 'Auxiliar diácono')
g_diacono_bloco, _ = Group.objects.get_or_create(name = 'Diácono bloco')
g_diacono_geral, _ = Group.objects.get_or_create(name = 'Diácono geral')
g_presbitero, _ = Group.objects.get_or_create(name = 'Presbítero')
g_administrador, _ = Group.objects.get_or_create(name = 'Administrador')

## Criação dos ContentTypes
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
ct_telefone = ContentType.objects.get_for_model(models.Telefone)


## Criação das permissões para o model Pessoa
p_self_pessoa, _ = Permission.objects.get_or_create(codename = 'view_self_pessoa',
                                    name = 'Pode ver próprio dado',
                                    content_type = ct_pessoa)
p_funcao_pessoa, _ = Permission.objects.get_or_create(codename = 'cannot_change_funcao_pessoa',
                                    name = 'Não pode editar função',
                                    content_type = ct_pessoa)

p_grupocaseiro_pessoa_view, _ = Permission.objects.get_or_create(codename = 'view_grupocaseiro_pessoa',
                                    name = 'Pode ver grupo caseiro',
                                    content_type = ct_pessoa)
p_grupocaseiro_pessoa_change, _ = Permission.objects.get_or_create(codename = 'change_grupocaseiro_pessoa',
                                    name = 'Pode editar grupo caseiro',
                                    content_type = ct_pessoa)

p_grupocaseiro_bloco_pessoa_view, _ = Permission.objects.get_or_create(codename = 'view_grupocaseiro_bloco_pessoa',
                                    name = 'Pode ver grupos caseiros do mesmo bloco',
                                    content_type = ct_pessoa)
p_grupocaseiro_bloco_pessoa_change, _ = Permission.objects.get_or_create(codename = 'change_grupocaseiro_bloco_pessoa',
                                    name = 'Pode editar grupos caseiros do mesmo bloco',
                                    content_type = ct_pessoa)


p_pessoa_add = Permission.objects.get(codename = 'add_pessoa',
                                       content_type = ct_pessoa)
p_pessoa_change = Permission.objects.get(codename = 'change_pessoa',
                                       content_type = ct_pessoa)
p_pessoa_view = Permission.objects.get(codename = 'view_pessoa',
                                       content_type = ct_pessoa)

# Criação das permissões para o model GrupoCaseiro
p_grupo_caseiro_add = Permission.objects.get(codename = 'add_grupocaseiro',
                                                content_type = ct_grupo_caseiro)
p_grupo_caseiro_change = Permission.objects.get(codename = 'change_grupocaseiro',
                                                content_type = ct_grupo_caseiro)
p_grupo_caseiro_view = Permission.objects.get(codename = 'view_grupocaseiro',
                                                content_type = ct_grupo_caseiro)

## Criação das permissões para o model MotivoAfastamento
p_motivo_afastamento_add = Permission.objects.get(codename = 'add_motivoafastamento',
                                       content_type = ct_motivo_afastamento)
p_motivo_afastamento_change = Permission.objects.get(codename = 'change_motivoafastamento',
                                       content_type = ct_motivo_afastamento)
p_motivo_afastamento_view = Permission.objects.get(codename = 'view_motivoafastamento',
                                       content_type = ct_motivo_afastamento)

## Criação das permissões para o model OrigemDiscipulo
p_origem_discipulo_add = Permission.objects.get(codename = 'add_origemdiscipulo',
                                       content_type = ct_origem_discipulo)
p_origem_discipulo_change = Permission.objects.get(codename = 'change_origemdiscipulo',
                                       content_type = ct_origem_discipulo)
p_origem_discipulo_view = Permission.objects.get(codename = 'view_origemdiscipulo',
                                       content_type = ct_origem_discipulo)

## Criação das permissões para o model Profissao
p_profissao_add = Permission.objects.get(codename = 'add_profissao',
                                       content_type = ct_profissao)
p_profissao_change = Permission.objects.get(codename = 'change_profissao',
                                       content_type = ct_profissao)
p_profissao = Permission.objects.get(codename = 'view_profissao',
                                       content_type = ct_profissao)

## Criação das permissões para o model EstadoCivil
p_estado_civil_add= Permission.objects.get(codename = 'add_estadocivil',
                                       content_type = ct_estado_civil)
p_estado_civil_change= Permission.objects.get(codename = 'change_estadocivil',
                                       content_type = ct_estado_civil)
p_estado_civil_view= Permission.objects.get(codename = 'view_estadocivil',
                                       content_type = ct_estado_civil)

## Criação das permissões para o model Bloco
p_bloco_add = Permission.objects.get(codename = 'add_bloco',
                                       content_type = ct_bloco)
p_bloco_change = Permission.objects.get(codename = 'change_bloco',
                                       content_type = ct_bloco)
p_bloco_view = Permission.objects.get(codename = 'view_bloco',
                                       content_type = ct_bloco)

## Criação das permissões para o model Localidade
p_localidade_add = Permission.objects.get(codename = 'add_localidade',
                                       content_type = ct_localidade)
p_localidade_change = Permission.objects.get(codename = 'change_localidade',
                                       content_type = ct_localidade)
p_localidade_view = Permission.objects.get(codename = 'view_localidade',
                                       content_type = ct_localidade)

## Criação das permissões para o model Funcao
p_funcao_add = Permission.objects.get(codename = 'add_funcao',
                                       content_type = ct_funcao)
p_funcao_change = Permission.objects.get(codename = 'change_funcao',
                                       content_type = ct_funcao)
p_funcao_view = Permission.objects.get(codename = 'view_funcao',
                                       content_type = ct_funcao)

## Criação das permissões para o model NivelServico
p_nivel_servico_add = Permission.objects.get(codename = 'add_nivelservico',
                                       content_type = ct_nivel_servico)
p_nivel_servico_change = Permission.objects.get(codename = 'change_nivelservico',
                                       content_type = ct_nivel_servico)
p_nivel_servico_view = Permission.objects.get(codename = 'view_nivelservico',
                                       content_type = ct_nivel_servico)

## Criação das permissões para o model Telefone
p_telefone_add = Permission.objects.get(codename = 'add_telefone',
                                       content_type = ct_telefone)
p_telefone_change = Permission.objects.get(codename = 'change_telefone',
                                       content_type = ct_telefone)
p_telefone_view = Permission.objects.get(codename = 'view_telefone',
                                       content_type = ct_telefone)

# Associando grupos às permissões
g_discipulo.permissions.add(p_funcao_pessoa, p_self_pessoa, p_pessoa_view, p_pessoa_change)

g_auxiliar_diacono.permissions.add(p_grupocaseiro_pessoa_view, p_grupocaseiro_pessoa_change, p_pessoa_view, p_pessoa_change, p_pessoa_add)

g_lider_g_caseiro.permissions.add(p_grupocaseiro_pessoa_view, p_pessoa_view)

g_diacono_bloco.permissions.add(p_grupocaseiro_bloco_pessoa_view, p_grupocaseiro_bloco_pessoa_change, p_pessoa_view, p_pessoa_change, p_pessoa_add)

g_diacono_geral.permissions.add(p_pessoa_view, p_grupo_caseiro_add, p_grupocaseiro_pessoa_change, p_pessoa_change, p_pessoa_add, p_grupo_caseiro_change, p_grupo_caseiro_view)

g_presbitero.permissions.add(p_pessoa_view)

g_administrador.permissions.add(p_pessoa_add, p_pessoa_change, p_pessoa_view, p_grupo_caseiro_add, p_grupo_caseiro_change, p_grupo_caseiro_view, p_motivo_afastamento_add, p_motivo_afastamento_change, p_motivo_afastamento_view, p_origem_discipulo_view, p_origem_discipulo_add, p_origem_discipulo_change, p_profissao_add, p_profissao_change, p_profissao, p_estado_civil_add, p_estado_civil_change, p_estado_civil_view, p_bloco_add, p_bloco_change, p_bloco_view, p_localidade_add, p_localidade_change, p_localidade_view, p_funcao_add, p_funcao_change, p_funcao_view, p_nivel_servico_add, p_nivel_servico_change, p_nivel_servico_view, p_telefone_add, p_telefone_change, p_telefone_view)


# Associando usuários aos groups
g_discipulo.user_set.add(discipulo)
g_lider_g_caseiro.user_set.add(lider)
g_auxiliar_diacono.user_set.add(auxiliar_diacono)
g_diacono_bloco.user_set.add(diacono_bloco)
g_diacono_geral.user_set.add(diacono_geral)
g_presbitero.user_set.add(presbitero)
g_administrador.user_set.add(administrador)









