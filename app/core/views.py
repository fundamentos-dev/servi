from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
from app.core.models import Pessoa

# Create your views here.

def manage_access(user):
    # Permissões negadas
    permissions_list = ['core.view_self_pessoa']

    for permission in permissions_list:
        if user.has_perm(permission) == False:
           return True

    return False

@login_required(login_url='/admin/login')
@user_passes_test(manage_access)
def index(request):
    # Coletando todas as pessoas para serem visualizadas, no momento sem filtro de autorizações
    pessoas = Pessoa.objects.all()
    
    def calculateAge(birthDate): 
        today = datetime.date.today() 
        age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day)) 
    
        return age

    pessoas = [{
        'email': p.email,
        'username': p.username,
        'nome': p.nome,
        'apelido': p.apelido,
        'data_nascimento' : p.data_nascimento,
        'idade' : calculateAge(p.data_nascimento),
        'discipulo_vinculado': 'Sim' if p.discipulo_vinculado else 'Não',
        'data_vinculacao_igreja_local': p.data_vinculacao_igreja_local,
        'data_afastamento': p.data_afastamento,
        'sexo': p.sexo,
        'grupo_caseiro': p.grupo_caseiro,
    }for p in pessoas]

    return render(request, "relatorio.html", { "pessoas": pessoas })
