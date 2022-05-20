# Adicionando usuários de teste
from django.contrib.auth.models import Group, Permission
from app.core import models
from django.contrib.auth import get_user_model
from app.core.models import Bloco, Funcao, GrupoCaseiro, NivelServico
import datetime

# Selecionando Nível de Serviço
nivel_servico_lider = NivelServico.objects.get(id=6)
nivel_servico_presbitero = NivelServico.objects.get(id=8)

# Selecionando Função
funcao_auxiliar_diacono = Funcao.objects.get(id=1)
funcao_diacono_bloco = Funcao.objects.get(id=2)
funcao_diacono_geral = Funcao.objects.get(id=3)
funcao_presbitero = Funcao.objects.get(id=4)
funcao_administrador = Funcao.objects.get(id=5)

# Selecionando Bloco para teste
bloco = Bloco.objects.get(id=1)

# Criando Igreja na casa de Teste
grupo_caseiro, _ = GrupoCaseiro.objects.get_or_create(nome="Grupo Caseiro de Teste", bloco=bloco)

# Declarando variáveis de uso comum
birthdate = datetime.date(1995, 11, 1)
User = get_user_model()

# Criando usuários de teste
presbitero, _ = User.objects.get_or_create(nome="Presbítero de Teste", email="presbitero@teste.br", data_nascimento=birthdate, is_staff=True, is_active=True,
     grupo_caseiro=grupo_caseiro, nivel_servico=nivel_servico_presbitero, funcao=funcao_presbitero)
diacono_bloco, _ = User.objects.get_or_create(nome="Diácono Local de Teste", email="diaconolocal@teste.br",
     data_nascimento=birthdate, is_staff=True, is_active=True, funcao=funcao_diacono_bloco)
diacono_geral, _ = User.objects.get_or_create(nome="Diácono Geral de Teste", email="diaconogeral@teste.br",
     data_nascimento=birthdate, is_staff=True, is_active=True, funcao=funcao_diacono_geral)
lider, _ = User.objects.get_or_create(nome="Líder de Teste", email="lider@teste.br", data_nascimento=birthdate,
     is_staff=True, is_active=True, nivel_servico=nivel_servico_lider)
discipulo, _ = User.objects.get_or_create(nome="Discípulo de Teste", email="discipulo@teste.br",
     data_nascimento=birthdate, is_staff=True, is_active=True)
auxiliar_diacono, _ = User.objects.get_or_create(nome="Auxiliar de Diácono de Teste", email="auxiliardiacono@teste.br",
     data_nascimento=birthdate, is_staff=True, is_active=True, funcao=funcao_auxiliar_diacono)
administrador, _ = User.objects.get_or_create(nome="Administrador", email="administrador@teste.br",
     data_nascimento=birthdate, is_staff=True, is_active=True, funcao=funcao_administrador)

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

from app.core import models
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from app.core import models
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

g_discipulo, _ = Group.objects.get_or_create(name = 'Discípulo')
g_lider_g_caseiro, _ = Group.objects.get_or_create(name = 'Lider do gurpo caseiro')
g_auxiliar_diacono, _ = Group.objects.get_or_create(name = 'Auxiliar diácono')
g_diacono_bloco, _ = Group.objects.get_or_create(name = 'Diácono bloco')
g_diacono_geral, _ = Group.objects.get_or_create(name = 'Diácono geral')
g_presbitero, _ = Group.objects.get_or_create(name = 'Presbítero')
g_administrador, _ = Group.objects.get_or_create(name = 'Administrador')

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
ct_conjugue = ContentType.objects.get_for_model(models.Conjugue)
ct_junta_discipulado = ContentType.objects.get_for_model(models.JuntaDiscipulado)
ct_telefone = ContentType.objects.get_for_model(models.Telefone)


## Criação das permissões para o model Pessoa
p_discipulo, _ = Permission.objects.get_or_create(codename = 'pode_ver_editar_proprios_dados',
                                    name = 'Pode ver e editar os próprios dados',
                                    content_type = ct_pessoa)
p_auxiliar_diacono, _ = Permission.objects.get_or_create(codename = 'pode_ver_editar_discipulos_grupo_caseiro',
                                    name = 'Pode ver e editar os díscipulos do seu grupo caseiro',
                                    content_type = ct_pessoa)
p_lider_g_caseiro, _ = Permission.objects.get_or_create(codename = 'pode_ver_discipulos_grupo_caseiro',
                                    name = 'Pode ver os díscipulos do seu grupo caseiro',
                                    content_type = ct_pessoa)
p_diacono_bloco, _ = Permission.objects.get_or_create(codename = 'pode_ver_proprio_bloco',
                                    name = 'Pode ver os díscipulos e grupo caseiro do seu bloco',
                                    content_type = ct_pessoa)

p_diacono_bloco_geral, _ = Permission.objects.get_or_create(codename = 'pode_editar_proprio_bloco',
                                    name = 'Pode editar os díscipulos e grupo caseiro do seu bloco',
                                    content_type = ct_pessoa)

p_presbitero_diacono_geral, _ = Permission.objects.get_or_create(codename = 'pode_ver_dados_toda_igreja',
                                    name = 'Pode ver todos os dados dos discípulos e grupo caseiro de toda igreja',
                                    content_type = ct_pessoa)

## Criação das permissões para o model GrupoCaseiro
p_diaconos, _ = Permission.objects.get_or_create(codename = 'pode_ver_editar_tabela_grupo_caseiro',
                                    name = 'Pode ver e editar a tabela grupo caseiro',
                                    content_type = ct_grupo_caseiro)


## Criação das permissões para o model MotivoAfastamento
p_motivo_afastamento, _ = Permission.objects.get_or_create(codename = 'pode_ver_editar_tabela_motivo_afastamento',
                                    name = 'Pode ver e editar a tabela motivo do afastamento',
                                    content_type = ct_motivo_afastamento)


## Criação das permissões para o model OrigemDiscipulo
p_origem_discipulo, _ = Permission.objects.get_or_create(codename = 'pode_ver_editar_tabela_origem_discipulo',
                                    name = 'Pode ver e editar a tabela origem do discípulo',
                                    content_type = ct_origem_discipulo)


## Criação das permissões para o model Profissao
p_profissao, _ = Permission.objects.get_or_create(codename = 'pode_ver_editar_tabela_profissao',
                                    name = 'Pode ver e editar a tabela profissão',
                                    content_type = ct_profissao)


## Criação das permissões para o model EstadoCivil
p_estado_civil, _= Permission.objects.get_or_create(codename = 'pode_ver_editar_tabela_estado_civil',
                                    name = 'Pode ver e editar a tabela estado civil',
                                    content_type = ct_estado_civil)


## Criação das permissões para o model Bloco
p_bloco, _ = Permission.objects.get_or_create(codename = 'pode_ver_editar_tabela_bloco',
                                    name = 'Pode ver e editar a tabela bloco',
                                    content_type = ct_bloco)


## Criação das permissões para o model Localidade
p_localidade, _ = Permission.objects.get_or_create(codename = 'pode_ver_editar_tabela_localidade',
                                    name = 'Pode ver e editar a tabela localidade',
                                    content_type = ct_localidade)


## Criação das permissões para o model Funcao
p_funcao, _ = Permission.objects.get_or_create(codename = 'pode_ver_editar_tabela_funcao',
                                    name = 'Pode ver e editar a tabela função',
                                    content_type = ct_funcao)


## Criação das permissões para o model NivelServico
p_nivel_servico, _ = Permission.objects.get_or_create(codename = 'pode_ver_editar_tabela_nivel_servico',
                                    name = 'Pode ver e editar a tabela nível serviço',
                                    content_type = ct_nivel_servico)


## Criação das permissões para o model Conjugue
p_conjugue, _ = Permission.objects.get_or_create(codename = 'pode_ver_editar_tabela_conjugue',
                                    name = 'Pode ver e editar a tabela conjugue',
                                    content_type = ct_conjugue)


## Criação das permissões para o model JuntaDiscipulado
p_junta_discipulado, _ = Permission.objects.get_or_create(codename = 'pode_ver_editar_tabela_junta_discipulado',
                                    name = 'Pode ver e editar a tabela junta discipulado',
                                    content_type = ct_junta_discipulado)


## Criação das permissões para o model Telefone
p_telefone, _ = Permission.objects.get_or_create(codename = 'pode_ver_editar_tabela_telefone',
                                    name = 'Pode ver e editar a tabela telefone',
                                    content_type = ct_telefone)



# Associando grupos às permissões
g_discipulo.permissions.add(p_discipulo)
g_auxiliar_diacono.permissions.add(p_auxiliar_diacono)
g_lider_g_caseiro.permissions.add(p_lider_g_caseiro)
g_diacono_bloco.permissions.add(p_diacono_bloco,
                                p_diacono_bloco_geral,
                                p_diaconos)
g_diacono_geral.permissions.add(p_presbitero_diacono_geral,
                                p_diacono_bloco_geral,
                                p_diaconos)
g_presbitero.permissions.add(p_presbitero_diacono_geral)

# Associando usuários aos groups
g_discipulo.user_set.add(discipulo)