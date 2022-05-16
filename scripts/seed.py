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
colaborador = User.objects.get(name="colaborador")
colaborador.set_password("passw@rd")