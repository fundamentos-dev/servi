from django.contrib import admin
from .models import Pessoa

@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'nome', 'data_nascimento', 'discipulo_vinculado', 'apelido', 'data_vinculacao_igreja_local', \
                    'data_afastamento', 'sexo')
    list_display_links = ('id', 'email', 'nome')
    search_fields = ('nome', 'email')

