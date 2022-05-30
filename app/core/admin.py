#from types import NoneType
import re
from app.core import models
from django.contrib import admin
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied, ValidationError
from django.forms import ModelForm
from django.http import Http404
from more_admin_filters import MultiSelectRelatedFilter
import csv
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string

'''
===============
TabularInline
===============
'''


class PessoaInline(admin.TabularInline):
    model = models.Pessoa


class GrupoCaseiroInline(admin.TabularInline):
    model = models.GrupoCaseiro


class TelefoneInline(admin.TabularInline):
    model = models.Telefone
    extra = 1


'''
===============
Registrando Admin
===============
'''


@admin.register(models.Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    # Populando campos padrões do admin
    list_display = ('id', 'email', 'nome', 'data_nascimento', 'apelido', 'discipulo_vinculado', 'data_vinculacao_igreja_local',
                    'data_afastamento', 'sexo', 'funcao', 'estado_civil', 'grupo_caseiro', 'localidade', 'nivel_servico', 'origem', 'profissao', 'pai', 'mae', 'conjuge')
    fields = ['email', 'nome', 'apelido', 'sexo', 'funcao', 'grupo_caseiro', 'localidade', 'nivel_servico', 'origem', 'profissao', 'pai', 'mae', 'companheiros', 'discipuladores', 'data_vinculacao_igreja_local', 'data_afastamento', 'estado_civil']
    list_display_links = ('id', 'email', 'nome')
    search_fields = ('nome', 'email')
    # https://github.com/thomst/django-more-admin-filters
    list_filter = [('estado_civil', MultiSelectRelatedFilter),
                   ('nivel_servico', MultiSelectRelatedFilter), 'grupo_caseiro']
    raw_id_fields = ['mae', 'pai', 'companheiros', 'conjuge', 'discipuladores']
    autocomplete_fields = ['pai', 'mae']
    inlines = [
        TelefoneInline,
    ]
    actions = ['download_csv']
    
    def download_csv(self, request, queryset):
        with open('relatorio.csv', 'wt') as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(['id', 'email', 'nome', 'data_nascimento', 'apelido', 'discipulo_vinculado', 'data_vinculacao_igreja_local',
                        'data_afastamento', 'sexo', 'funcao', 'estado_civil', 'grupo_caseiro', 'localidade', 'nivel_servico', 'origem', 'profissao', 'pai', 'mae', 'conjuge'])
            for dado in queryset:
                writer.writerow([dado.id, dado.email, dado.nome, dado.data_nascimento, dado.apelido, dado.discipulo_vinculado, dado.data_vinculacao_igreja_local, dado.data_afastamento, dado.sexo, dado.funcao, dado.estado_civil, dado.grupo_caseiro, dado.localidade, dado.nivel_servico, dado.origem, dado.profissao, dado.pai, dado.mae, dado.conjuge])    
            
        with open('relatorio.csv', 'r') as arquivo:
            response = HttpResponse(arquivo, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=relatorio.csv'
            return response
    download_csv.short_description = "Download CSV."

    # Criando regras para visualização de registro de acordo com as permissões
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Apresentando as informações de acordo com o tipo de usuário
        if request.user.has_perm('core.view_self_pessoa') and not request.user.is_superuser:
            return qs.filter(email=request.user.email)
        elif request.user.has_perm('core.view_grupocaseiro_pessoa') and not request.user.is_superuser:
            return qs.filter(grupo_caseiro=request.user.grupo_caseiro)
        elif request.user.has_perm('core.view_grupocaseiro_bloco_pessoa') and not request.user.is_superuser:
            return qs.filter(grupo_caseiro__bloco_id=request.user.grupo_caseiro.bloco.id)
        return qs.all()

    # Editando o método save_model
    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)
        # Atribuindo o obejeto de cada grupo a uma variável
        g_lider_caseiro = Group.objects.get(name='Lider do gurpo caseiro')
        g_presbitero = Group.objects.get(name='Presbítero')
        g_discipulo = Group.objects.get(name='Discípulo')
        g_auxiliar_diacono = Group.objects.get(name='Auxiliar diácono')
        g_diacono_bloco = Group.objects.get(name='Diácono bloco')
        g_diacono_geral = Group.objects.get(name='Diácono geral')
        g_administrador = Group.objects.get(name='Administrador')

        # Testanando qual o nível de serviço/função do usuário adicionado e atribuindo o grupo dinamicamente
        if obj.nivel_servico is not None:
            if obj.nivel_servico.id == 6:
                g_lider_caseiro.user_set.add(obj)
            elif obj.nivel_servico.id == 8 and obj.funcao.id == 4:
                g_presbitero.user_set.add(obj)
        elif obj.funcao is not None:
            print(obj.funcao.id)
            if obj.funcao.id == 1:
                g_auxiliar_diacono.user_set.add(obj)
            elif obj.funcao.id == 2:
                g_diacono_bloco.user_set.add(obj)
            elif obj.funcao.id == 3:
                g_diacono_geral.user_set.add(obj)
            elif obj.funcao.id == 5:
                g_administrador.user_set.add(obj)
            else:
                g_discipulo.user_set.add(obj)
        if obj.discipulo_vinculado:
            g_discipulo.user_set.add(obj)
            
        if obj.estado_civil is not None:
            if obj.estado_civil.id == 2:
                if not 'conjuge' in self.fields:
                    self.fields.append('conjuge')
            else:
                if 'conjuge' in self.fields:
                    i = self.fields.index('conjuge')
                    del self.fields[i]
                

        if obj.data_vinculacao_igreja_local is not None:
            if not 'discipulo_vinculado' in self.fields:
                self.fields.append('discipulo_vinculado')
        else:
             if 'discipulo_vinculado' in self.fields:
                    i = self.fields.index('discipulo_vinculado')
                    del self.fields[i]           
            
    
        if obj.data_afastamento is not None:
            if not 'motivo_afastamento' in self.fields:
                print(type(self.fields))
                self.fields.append('motivo_afastamento')
        else:
            if 'motivo_afastamento' in self.fields:
                    i = self.fields.index('motivo_afastamento')
                    del self.fields[i]   
            

    # Criando regras para edição de regristros de acordo com as permissões

    def get_form(self, request, obj=None, **kwargs):
        # Formulário para editar pessoas
        qs = super().get_queryset(request)
        form = super().get_form(request, obj, **kwargs)
        disabled_fields = set()  # type: Set[str]

        
        
        # Validando os campos de acordo com as permissões
        if request.user.has_perm('core.cannot_change_funcao_pessoa') and not request.user.is_superuser:
            disabled_fields |= {
                'funcao',
                'nivel_servico',
                'motivo_afastamento',
                'data_afastamento',
                'grupo_caseiro'
            }
        elif request.user.has_perm('core.change_grupocaseiro_pessoa') and not request.user.is_superuser:
            if request.user.grupo_caseiro:
                filtro = list(
                    qs.filter(grupo_caseiro=request.user.grupo_caseiro))
                url = str(request.get_full_path)
                id_form = int(re.sub('[^0-9]', '', url))
                controle = False
                for pessoa in filtro:
                    id = pessoa.id
                    if id_form == id:
                        controle = True
                if not controle:
                    raise ValueError('Não tem autorização para acessar a página')
        elif request.user.has_perm('core.change_grupocaseiro_bloco_pessoa') and not request.user.is_superuser:
            if request.user.grupo_caseiro.bloco.id:
                filtro = list(
                    qs.filter(grupo_caseiro__bloco_id=request.user.grupo_caseiro.bloco.id))
                url = str(request.get_full_path)
                id_form = int(re.sub('[^0-9]', '', url))
                controle = False
            for pessoa in filtro:
                id = pessoa.id
                if id_form == id:
                    controle = True
            if not controle:
                raise ValueError('Não tem autorização para acessar a página')

        # Criando laço para pecorrer os campos desabiltados
        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form

admin.site.register(models.MotivoAfastamento)
admin.site.register(models.OrigemDiscipulo)
admin.site.register(models.Profissao)
admin.site.register(models.EstadoCivil)
admin.site.register(models.GrupoCaseiro)
admin.site.register(models.Bloco)
admin.site.register(models.Localidade)
admin.site.register(models.Funcao)
admin.site.register(models.NivelServico)
admin.site.register(models.Telefone)
