from django.shortcuts import render
from django.http import HttpResponse
import datetime

from app.core.models import Pessoa

# Create your views here.


def index(request):
    # Coletando todas as pessoas para serem visualizadas, no momento sem filtro de autorizações
    pessoas = Pessoa.objects.all()
    return render(request, "relatorio.html", { "pessoas": pessoas })
