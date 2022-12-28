# Adicionando usuários de teste
import datetime
import random
import csv
import os

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

from app.settings import BASE_DIR
from app.core import models
from app.core.models import Bloco, Funcao, GrupoCaseiro, NivelServico, EstadoCivil, Localidade

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
bloco_2 = Bloco.objects.get(id=2)
bloco_3 = Bloco.objects.get(id=3)

# Criando Igreja na casa de Teste
grupo_caseiro, _ = GrupoCaseiro.objects.get_or_create(nome="Grupo Caseiro de Teste 1", bloco=bloco)
grupo_caseiro_2, _ = GrupoCaseiro.objects.get_or_create(nome="Grupo Caseiro de Teste 2", bloco=bloco_2)
grupo_caseiro_3, _ = GrupoCaseiro.objects.get_or_create(nome="Grupo Caseiro de Teste 3", bloco=bloco_3)
grupo_caseiro_4, _ = GrupoCaseiro.objects.get_or_create(nome="Grupo Caseiro de Teste 4", bloco=bloco)

# Declarando variáveis de uso comum
date = datetime.date(1995, 11, 1)
User = get_user_model()
password = 'passw@rd'

# Criando usuários de teste
presbitero = User.objects.create_user(nome="Presbítero de Teste", email="presbitero@teste.br", data_nascimento=date, is_staff=True, is_active=True, grupo_caseiro=grupo_caseiro_3, nivel_servico=nivel_servico_presbitero, funcao=funcao_presbitero, estado_civil=estado_civil_solteiro, data_vinculacao_igreja_local=date, password=password)
diacono_bloco = User.objects.create_user(nome="Diácono Local de Teste", email="diaconolocal@teste.br",
     data_nascimento=date, grupo_caseiro=grupo_caseiro_2, is_staff=True, is_active=True, funcao=funcao_diacono_bloco, estado_civil=estado_civil_casado, data_vinculacao_igreja_local=date, password=password)
diacono_geral = User.objects.create_user(nome="Diácono Geral de Teste", email="diaconogeral@teste.br",
     data_nascimento=date, grupo_caseiro=grupo_caseiro_3, is_staff=True, is_active=True, funcao=funcao_diacono_geral, estado_civil=estado_civil_casado, password=password)
lider = User.objects.create_user(nome="Líder de Teste", email="lider@teste.br", data_nascimento=date,
     is_staff=True, is_active=True, grupo_caseiro=grupo_caseiro, nivel_servico=nivel_servico_lider, estado_civil=estado_civil_solteiro, data_vinculacao_igreja_local=date, password=password)
discipulo = User.objects.create_user(nome="Discípulo de Teste", email="discipulo@teste.br",
     data_nascimento=date, is_staff=True, grupo_caseiro=grupo_caseiro, is_active=True, estado_civil=estado_civil_casado, password=password)
auxiliar_diacono = User.objects.create_user(nome="Auxiliar de Diácono de Teste", email="auxiliardiacono@teste.br",
     data_nascimento=date, is_staff=True, grupo_caseiro=grupo_caseiro, is_active=True, funcao=funcao_auxiliar_diacono, estado_civil=estado_civil_divorciado, data_vinculacao_igreja_local=date, password=password)
administrador = User.objects.create_user(nome="Administrador", email="administrador@teste.br",
     data_nascimento=date, is_staff=True, grupo_caseiro=grupo_caseiro, is_active=True, funcao=funcao_administrador, estado_civil=estado_civil_divorciado, password=password)


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


## Criação de Permissões para o model Pessoa
p_self_pessoa_read, _ = Permission.objects.get_or_create(codename = 'view_self_pessoa', name = 'Pode ver próprio dado', content_type = ct_pessoa)
p_funcao_pessoa_cannot_update, _ = Permission.objects.get_or_create(codename = 'cannot_change_funcao_pessoa', name = 'Não pode editar função', content_type = ct_pessoa)
p_grupocaseiro_pessoa_read, _ = Permission.objects.get_or_create(codename = 'view_grupocaseiro_pessoa', name = 'Pode ver pessoas do mesmo grupo caseiro que elas e relacionadas', content_type = ct_pessoa)
p_grupocaseiro_pessoa_update, _ = Permission.objects.get_or_create(codename = 'change_grupocaseiro_pessoa', name = 'Pode editar pessoas do mesmo grupo caseiro que elas', content_type = ct_pessoa)
p_grupocaseiro_bloco_pessoa_read, _ = Permission.objects.get_or_create(codename = 'view_grupocaseiro_bloco_pessoa', name = 'Pode ver grupos caseiros do mesmo bloco', content_type = ct_pessoa)
p_grupocaseiro_bloco_pessoa_update, _ = Permission.objects.get_or_create(codename = 'change_grupocaseiro_bloco_pessoa', name = 'Pode editar grupos caseiros do mesmo bloco', content_type = ct_pessoa)

# Permissões Django do model Pessoa
p_pessoa_create = Permission.objects.get(codename = 'add_pessoa', content_type = ct_pessoa)
p_pessoa_read = Permission.objects.get(codename = 'view_pessoa', content_type = ct_pessoa)
p_pessoa_update = Permission.objects.get(codename = 'change_pessoa', content_type = ct_pessoa)
p_pessoa_delete = Permission.objects.get(codename = 'delete_pessoa', content_type = ct_pessoa)

# Permissões Django do model GrupoCaseiro
p_grupo_caseiro_create = Permission.objects.get(codename = 'add_grupocaseiro', content_type = ct_grupo_caseiro)
p_grupo_caseiro_read = Permission.objects.get(codename = 'view_grupocaseiro', content_type = ct_grupo_caseiro)
p_grupo_caseiro_update = Permission.objects.get(codename = 'change_grupocaseiro', content_type = ct_grupo_caseiro)
p_grupo_caseiro_delete = Permission.objects.get(codename = 'delete_grupocaseiro', content_type = ct_grupo_caseiro)

## Permissões Django do model MotivoAfastamento
p_motivo_afastamento_create = Permission.objects.get(codename = 'add_motivoafastamento', content_type = ct_motivo_afastamento)
p_motivo_afastamento_read = Permission.objects.get(codename = 'view_motivoafastamento', content_type = ct_motivo_afastamento)
p_motivo_afastamento_update = Permission.objects.get(codename = 'change_motivoafastamento', content_type = ct_motivo_afastamento)
p_motivo_afastamento_delete = Permission.objects.get(codename = 'delete_motivoafastamento', content_type = ct_motivo_afastamento)

## Permissões Django do model OrigemDiscipulo
p_origem_discipulo_create = Permission.objects.get(codename = 'add_origemdiscipulo', content_type = ct_origem_discipulo)
p_origem_discipulo_read = Permission.objects.get(codename = 'view_origemdiscipulo', content_type = ct_origem_discipulo)
p_origem_discipulo_update = Permission.objects.get(codename = 'change_origemdiscipulo', content_type = ct_origem_discipulo)
p_origem_discipulo_delete = Permission.objects.get(codename = 'delete_origemdiscipulo', content_type = ct_origem_discipulo)

## Permissões Django do model Profissao
p_profissao_create = Permission.objects.get(codename = 'add_profissao', content_type = ct_profissao)
p_profissao_read = Permission.objects.get(codename = 'view_profissao', content_type = ct_profissao)
p_profissao_update = Permission.objects.get(codename = 'change_profissao', content_type = ct_profissao)
p_profissao_delete = Permission.objects.get(codename = 'delete_profissao', content_type = ct_profissao)

## Permissões Django do model EstadoCivil
p_estado_civil_create = Permission.objects.get(codename = 'add_estadocivil', content_type = ct_estado_civil)
p_estado_civil_read = Permission.objects.get(codename = 'view_estadocivil', content_type = ct_estado_civil)
p_estado_civil_update = Permission.objects.get(codename = 'change_estadocivil', content_type = ct_estado_civil)
p_estado_civil_delete = Permission.objects.get(codename = 'delete_estadocivil', content_type = ct_estado_civil)

## Permissões Django do model Bloco
p_bloco_create = Permission.objects.get(codename = 'add_bloco', content_type = ct_bloco)
p_bloco_read = Permission.objects.get(codename = 'view_bloco', content_type = ct_bloco)
p_bloco_update = Permission.objects.get(codename = 'change_bloco', content_type = ct_bloco)
p_bloco_delete = Permission.objects.get(codename = 'delete_bloco', content_type = ct_bloco)

## Permissões Django do model Localidade
p_localidade_create = Permission.objects.get(codename = 'add_localidade', content_type = ct_localidade)
p_localidade_read = Permission.objects.get(codename = 'view_localidade', content_type = ct_localidade)
p_localidade_update = Permission.objects.get(codename = 'change_localidade', content_type = ct_localidade)
p_localidade_delete = Permission.objects.get(codename = 'delete_localidade', content_type = ct_localidade)

## Permissões Django do model Funcao
p_funcao_create = Permission.objects.get(codename = 'add_funcao', content_type = ct_funcao)
p_funcao_read = Permission.objects.get(codename = 'view_funcao', content_type = ct_funcao)
p_funcao_update = Permission.objects.get(codename = 'change_funcao', content_type = ct_funcao)
p_funcao_delete = Permission.objects.get(codename = 'delete_funcao', content_type = ct_funcao)

## Permissões Django do model NivelServico
p_nivel_servico_create = Permission.objects.get(codename = 'add_nivelservico', content_type = ct_nivel_servico)
p_nivel_servico_update = Permission.objects.get(codename = 'change_nivelservico', content_type = ct_nivel_servico)
p_nivel_servico_read = Permission.objects.get(codename = 'view_nivelservico', content_type = ct_nivel_servico)
p_nivel_servico_delete = Permission.objects.get(codename = 'delete_nivelservico', content_type = ct_nivel_servico)

## Permissões Django do model Telefone
p_telefone_create = Permission.objects.get(codename = 'add_telefone', content_type = ct_telefone)
p_telefone_read = Permission.objects.get(codename = 'view_telefone', content_type = ct_telefone)
p_telefone_update = Permission.objects.get(codename = 'change_telefone', content_type = ct_telefone)
p_telefone_delete = Permission.objects.get(codename = 'delete_telefone', content_type = ct_telefone)

# Associando grupos às permissões
g_discipulo.permissions.add(p_funcao_pessoa_cannot_update, p_self_pessoa_read, p_pessoa_read, p_pessoa_update, p_telefone_create, p_telefone_read, p_telefone_update, p_telefone_delete)
g_auxiliar_diacono.permissions.add(p_grupocaseiro_pessoa_read, p_grupocaseiro_pessoa_update, p_pessoa_read, p_pessoa_update, p_pessoa_create)
g_lider_g_caseiro.permissions.add(p_grupocaseiro_pessoa_read, p_pessoa_read, p_grupocaseiro_pessoa_update, p_pessoa_update, p_pessoa_create)
g_diacono_bloco.permissions.add(p_grupocaseiro_bloco_pessoa_read, p_grupocaseiro_bloco_pessoa_update, p_pessoa_read, p_pessoa_update, p_pessoa_create)
g_diacono_geral.permissions.add(p_pessoa_read, p_grupo_caseiro_create, p_grupocaseiro_pessoa_update, p_pessoa_update, p_pessoa_create, p_grupo_caseiro_update, p_grupo_caseiro_read)
g_presbitero.permissions.add(p_pessoa_read)
g_administrador.permissions.add(
     p_pessoa_create, p_pessoa_update, p_pessoa_read, p_pessoa_delete, 
     p_grupo_caseiro_create, p_grupo_caseiro_update, p_grupo_caseiro_read, 
     p_motivo_afastamento_create, p_motivo_afastamento_update, p_motivo_afastamento_read, 
     p_origem_discipulo_read, p_origem_discipulo_create, p_origem_discipulo_update, 
     p_profissao_create, p_profissao_update, p_profissao_read, 
     p_estado_civil_create, p_estado_civil_update, p_estado_civil_read, 
     p_bloco_create, p_bloco_update, p_bloco_read, 
     p_localidade_create, p_localidade_update, p_localidade_read, 
     p_funcao_create, p_funcao_update, p_funcao_read, 
     p_nivel_servico_create, p_nivel_servico_update, p_nivel_servico_read, p_nivel_servico_delete, 
     p_telefone_create, p_telefone_update, p_telefone_read, p_telefone_delete)


# Associando usuários aos groups
g_discipulo.user_set.add(discipulo)
g_lider_g_caseiro.user_set.add(lider)
g_auxiliar_diacono.user_set.add(auxiliar_diacono)
g_diacono_bloco.user_set.add(diacono_bloco)
g_diacono_geral.user_set.add(diacono_geral)
g_presbitero.user_set.add(presbitero)
g_administrador.user_set.add(administrador)


# Criando contas fakes
from faker import Faker
fake = Faker()

groups = [
     g_discipulo,
     g_lider_g_caseiro,
     g_auxiliar_diacono,
     g_diacono_bloco,
     g_diacono_geral,
     g_presbitero,
     g_administrador
]

estados_civis = EstadoCivil.objects.all()
niveis_servico = NivelServico.objects.all()
grupos_caseiro = GrupoCaseiro.objects.all()

for _ in range(45):

     try:
          user = User.objects.create_user(nome=fake.name(), email=fake.email(), data_nascimento=fake.date(), is_staff=True, is_active=True, grupo_caseiro=random.choice(grupos_caseiro), nivel_servico=random.choice(niveis_servico), estado_civil=random.choice(estados_civis), data_vinculacao_igreja_local=fake.date(), password=password, sexo=random.choice(['M', 'F']))

          group = random.choice(groups)
          group.user_set.add(user)

     except Exception as e:
          print(e)

with open(os.path.join(BASE_DIR, "app/localidades.csv"), 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
    localidade = Localidade.objects.create(nome=row[0])
    print(f'Adicionando localidade: {localidade.nome}')
    localidade.save()