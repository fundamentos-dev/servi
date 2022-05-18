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