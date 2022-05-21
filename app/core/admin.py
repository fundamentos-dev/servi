#from types import NoneType
import re

from app.core import models
from django.contrib import admin
from django.core.exceptions import PermissionDenied, ValidationError
from django.forms import ModelForm
from django.http import Http404
from more_admin_filters import MultiSelectRelatedFilter


'''
===============
TabularInline
===============
'''

class PessoaInline(admin.TabularInline):
    model = models.Pessoa


class GrupoCaseiroInline(admin.TabularInline):
    model = models.GrupoCaseiro

class ConjugueInline(admin.TabularInline):
    model = models.Conjugue
    

class JuntaDiscipuladoInline(admin.TabularInline):
    model = models.JuntaDiscipulado
    
    
class TelefoneInline(admin.TabularInline):
    model = models.Telefone    
    
    
    '''
    ===============
    Registrando Admin
    ===============
    '''
@admin.register(models.Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    ## Populando campos padrões do admin
    list_display = ('id', 'email', 'nome', 'data_nascimento', 'discipulo_vinculado', 'apelido', 'data_vinculacao_igreja_local',
                    'data_afastamento', 'sexo', 'funcao', 'estado_civil', 'grupo_caseiro', 'localidade', 'nivel_servico', 'motivo_afastamento', 'origem', 'profissao', 'pai', 'mae')
    fields = ('email', 'nome', 'password', 'discipulo_vinculado', 'apelido', 'data_vinculacao_igreja_local',
                    'data_afastamento', 'sexo', 'funcao', 'estado_civil', 'grupo_caseiro', 'localidade', 'nivel_servico', 'motivo_afastamento', 'origem', 'profissao', 'pai', 'mae', 'companheiros')
    list_display_links = ('id', 'email', 'nome')
    search_fields = ('nome', 'email')
    # https://github.com/thomst/django-more-admin-filters
    list_filter = [('estado_civil', MultiSelectRelatedFilter), ('nivel_servico', MultiSelectRelatedFilter), 'grupo_caseiro']
    inline = [
        TelefoneInline, JuntaDiscipuladoInline, ConjugueInline
    ]

    ## Criando regras para visualização de registro de acordo com as permissões
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Apresentando as informações de acordo com o tipo de usuario
        if request.user.has_perm('core.view_self_pessoa') and not request.user.is_superuser:
            return qs.filter(email=request.user.email)
        elif request.user.has_perm('core.view_grupocaseiro_pessoa') and not request.user.is_superuser:
            return qs.filter(grupo_caseiro=request.user.grupo_caseiro)
        elif request.user.has_perm('core.view_grupocaseiro_bloco_pessoa') and not request.user.is_superuser:
            return qs.filter(grupo_caseiro__bloco_id=request.user.grupo_caseiro.bloco.id)
        return qs.all()


    ## Criando regras para edição de regristros de acordo com as permissões
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
                filtro = list(qs.filter(grupo_caseiro=request.user.grupo_caseiro))
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
                filtro = list(qs.filter(grupo_caseiro__bloco_id=request.user.grupo_caseiro.bloco.id))
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


@admin.register(models.MotivoAfastamento)
class MotivoAfastmentoAdmin(admin.ModelAdmin):
    inline = [
        PessoaInline,
    ]

@admin.register(models.OrigemDiscipulo)
class OrigemDiscipuloAdmin(admin.ModelAdmin):
     inline = [
        PessoaInline,
    ]

@admin.register(models.Profissao)
class ProfissaoAdmin(admin.ModelAdmin):
     inlines = [
        PessoaInline,
    ]

@admin.register(models.EstadoCivil)
class EstadoCivilAdmin(admin.ModelAdmin):
    inlines = [
        PessoaInline,
    ]


@admin.register(models.Bloco)
class BlocoAdmin(admin.ModelAdmin):
    inlines = [
        GrupoCaseiroInline,
    ]


@admin.register(models.GrupoCaseiro)
class GrupoCaseiroAdmin(admin.ModelAdmin):
     inlines = [
        PessoaInline,
    ]


@admin.register(models.Localidade)
class LocalidadeAdmin(admin.ModelAdmin):
    inlines = [
        PessoaInline,
    ]

@admin.register(models.Funcao)
class FuncaoAdmin(admin.ModelAdmin):
     inlines = [
        PessoaInline,
    ]

@admin.register(models.NivelServico)
class NivelServicoAdmin(admin.ModelAdmin):
     inlines = [
        PessoaInline,
    ]
@admin.register(models.Conjugue)
class ConjugueAdmin(admin.ModelAdmin):
    pass


@admin.register(models.JuntaDiscipulado)
class JuntaDiscipuladoAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Telefone)
class TelefoneAdmin(admin.ModelAdmin):
    pass
