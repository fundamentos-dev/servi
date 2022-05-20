#from types import NoneType
import re

from app.core import models
from django.contrib import admin
from django.core.exceptions import PermissionDenied, ValidationError
from django.forms import ModelForm
from django.http import Http404
from more_admin_filters import MultiSelectRelatedFilter


@admin.register(models.Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'nome', 'data_nascimento', 'discipulo_vinculado', 'apelido', 'data_vinculacao_igreja_local',
                    'data_afastamento', 'sexo', 'grupo')
    fields = ('email', 'nome', 'apelido', 'data_vinculacao_igreja_local',
              'data_afastamento', 'sexo', 'estado_civil', 'grupo_caseiro', 'pai', 'mae', 'funcao', 'groups', 'nivel_servico', 'grupo')
    list_display_links = ('id', 'email', 'nome')
    search_fields = ('nome', 'email')
    # https://github.com/thomst/django-more-admin-filters
    list_filter = [('estado_civil', MultiSelectRelatedFilter), ('nivel_servico', MultiSelectRelatedFilter), 'grupo_caseiro']


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Testando qual tipo de permissão tem o usuário
        request_discipulo = request.user.has_perm(
            'pode_ver_editar_proprios_dados') 
        request_lider_g_caseiro = request.user.has_perm(
            'pode_ver_discipulos_grupo_caseiro')
        request_auxiliar_diacono = request.user.has_perm(
            'pode_ver_editar_discipulos_grupo_caseiro')
        request_diacono_bloco = request.user.has_perm('pode_ver_proprio_bloco')
       

        # Apresentando as informações de acordo com o tipo de usuario
        if request_discipulo and not request.user.is_superuser:
            return qs.filter(email=request.user.email)
        elif request_lider_g_caseiro and request_auxiliar_diacono and not request.user.is_superuser:
            return qs.filter(grupo_caseiro=request.user.grupo_caseiro)
        elif request_diacono_bloco and not request.user.is_superuser:
            return qs.filter(grupo_caseiro__bloco_id=request.user.grupo_caseiro.bloco.id)
        return qs.all()

    def get_form(self, request, obj=None, **kwargs):
        # Formulário para editar pessoas
        qs = super().get_queryset(request)
        form = super().get_form(request, obj, **kwargs)
        disabled_fields = set()  # type: Set[str]

        # Validando os campos de acordo com as permissões
        if request.user.has_perm('pode_ver_editar_proprios_dados'):
            if not 'pai' in self.fields:
                self.fields = self.fields + ()
            disabled_fields |= {
                'grupo_caseiro',
                'data_afastamento',
                'motivo_afastamento',
                'data_vinculacao_igreja_local',
            }
        elif request.user.has_perm('pode_ver_discipulos_grupo_caseiro') and request.user.has_perm('nao_pode_editar') and not request.user.is_authenticated:
            raise PermissionDenied()
        elif request.user.has_perm('pode_editar_proprio_bloco'):
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
            if controle:
                disabled_fields |= {
                    'nome',
                }
            else:
                raise Http404()

        # Criando laço para pecorrer os campos desabiltados
        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form


@admin.register(models.MotivoAfastamento)
class MotivoAfastmentoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    fields = ('nome',)
    list_display_links = ('nome',)
    search_fields = ('nome',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Apresentando as informações de acordo com o tipo de usuario
        if request.user.has_perm('pode_ver_editar_tabela_motivo_afastamento'):
            return qs.all()
        else:
            raise Http404()

    def get_form(self, request, obj=None, **kwargs):
        # Formulário para editar pessoas
        qs = super().get_queryset(request)
        form = super().get_form(request, obj, **kwargs)
        disabled_fields = set()  # type: Set[str]

        # Validando os campos de acordo com as permissões
        if not request.user.has_perm('pode_ver_editar_tabela_motivo_afastamento'):
            raise Http404()

        return form


@admin.register(models.OrigemDiscipulo)
class OrigemDiscipuloAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    fields = ('nome',)
    list_display_links = ('nome',)
    search_fields = ('nome',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Apresentando as informações de acordo com o tipo de usuario
        if request.user.has_perm('pode_ver_editar_tabela_origem_discipulo'):
            return qs.all()
        else:
            raise Http404()

    def get_form(self, request, obj=None, **kwargs):
        # Formulário para editar pessoas
        qs = super().get_queryset(request)
        form = super().get_form(request, obj, **kwargs)
        disabled_fields = set()  # type: Set[str]

        # Validando os campos de acordo com as permissões
        if not request.user.has_perm('pode_ver_editar_tabela_origem_discipulo'):
            raise Http404()

        return form


@admin.register(models.Profissao)
class ProfissaoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    fields = ('nome',)
    list_display_links = ('nome',)
    search_fields = ('nome',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Apresentando as informações de acordo com o tipo de usuario
        if request.user.has_perm('pode_ver_editar_tabela_profissao'):
            return qs.all()
        else:
            raise Http404()

    def get_form(self, request, obj=None, **kwargs):
        # Formulário para editar pessoas
        qs = super().get_queryset(request)
        form = super().get_form(request, obj, **kwargs)
        disabled_fields = set()  # type: Set[str]

        # Validando os campos de acordo com as permissões
        if not request.user.has_perm('pode_ver_editar_tabela_profissao'):
            raise Http404()

        return form


@admin.register(models.EstadoCivil)
class EstadoCivilAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    fields = ('nome',)
    list_display_links = ('nome',)
    search_fields = ('nome',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Apresentando as informações de acordo com o tipo de usuario
        if request.user.has_perm('pode_ver_editar_tabela_estado_civil'):
            return qs.all()
        else:
            raise Http404()

    def get_form(self, request, obj=None, **kwargs):
        # Formulário para editar pessoas
        qs = super().get_queryset(request)
        form = super().get_form(request, obj, **kwargs)
        disabled_fields = set()  # type: Set[str]

        # Validando os campos de acordo com as permissões
        if not request.user.has_perm('pode_ver_editar_tabela_estado_civil'):
            raise Http404()

        return form


@admin.register(models.Bloco)
class BlocoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    fields = ('nome',)
    list_display_links = ('nome',)
    search_fields = ('nome',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Apresentando as informações de acordo com o tipo de usuario
        if request.user.has_perm('pode_ver_editar_tabela_bloco'):
            return qs.all()
        else:
            raise Http404()

    def get_form(self, request, obj=None, **kwargs):
        # Formulário para editar pessoas
        qs = super().get_queryset(request)
        form = super().get_form(request, obj, **kwargs)
        disabled_fields = set()  # type: Set[str]

        # Validando os campos de acordo com as permissões
        if not request.user.has_perm('pode_ver_editar_tabela_bloco'):
            raise Http404()

        return form


@admin.register(models.GrupoCaseiro)
class GrupoCaseiroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'bloco')
    fields = ('id', 'nome', 'bloco')
    list_display_links = ('id', 'nome', 'bloco')
    search_fields = ('id', 'nome', 'bloco')

    # def __init__(self, *args, **kwargs):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Retornando lista default para fins de teste
        return super().get_queryset(request)

        # Apresentando as informações de acordo com o tipo de usuario
        if request.user.has_perm('pode_ver_editar_tabela_grupo_caseiro'):
            return qs.filter(bloco_id=request.user.grupo_caseiro)

        raise PermissionDenied()


@admin.register(models.Localidade)
class LocalidadeAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    fields = ('nome',)
    list_display_links = ('nome',)
    search_fields = ('nome',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Apresentando as informações de acordo com o tipo de usuario
        if request.user.has_perm('pode_ver_editar_tabela_localidade'):
            return qs.all()
        else:
            raise Http404()

    def get_form(self, request, obj=None, **kwargs):
        # Formulário para editar pessoas
        qs = super().get_queryset(request)
        form = super().get_form(request, obj, **kwargs)
        disabled_fields = set()  # type: Set[str]

        # Validando os campos de acordo com as permissões
        if not request.user.has_perm('pode_ver_editar_tabela_localidade'):
            raise Http404()

        return form


@admin.register(models.Funcao)
class FuncaoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    fields = ('nome',)
    list_display_links = ('nome',)
    search_fields = ('nome',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Apresentando as informações de acordo com o tipo de usuario
        if request.user.has_perm('pode_ver_editar_tabela_funcao'):
            return qs.all()
        else:
            raise Http404()

    def get_form(self, request, obj=None, **kwargs):
        # Formulário para editar pessoas
        qs = super().get_queryset(request)
        form = super().get_form(request, obj, **kwargs)
        disabled_fields = set()  # type: Set[str]

        # Validando os campos de acordo com as permissões
        if not request.user.has_perm('pode_ver_editar_tabela_funcao'):
            raise Http404()

        return form


@admin.register(models.NivelServico)
class NivelServicoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    fields = ('nome',)
    list_display_links = ('nome',)
    search_fields = ('nome',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Apresentando as informações de acordo com o tipo de usuario
        if request.user.has_perm('pode_ver_editar_tabela_nivel_servico'):
            return qs.all()
        else:
            raise Http404()

    def get_form(self, request, obj=None, **kwargs):
        # Formulário para editar pessoas
        qs = super().get_queryset(request)
        form = super().get_form(request, obj, **kwargs)
        disabled_fields = set()  # type: Set[str]

        # Validando os campos de acordo com as permissões
        if not request.user.has_perm('pode_ver_editar_tabela_nivel_servico'):
            raise Http404()

        return form

@admin.register(models.Conjugue)
class ConjugueAdmin(admin.ModelAdmin):
    list_display = ('marido', 'esposa')
    fields = ('marido', 'esposa')
    list_display_links = ('marido', 'esposa')
    search_fields = ('marido', 'esposa')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Apresentando as informações de acordo com o tipo de usuario
        if request.user.has_perm('pode_ver_editar_tabela_conjugue'):
            return qs.all()
        else:
            raise Http404()

    def get_form(self, request, obj=None, **kwargs):
        # Formulário para editar pessoas
        qs = super().get_queryset(request)
        form = super().get_form(request, obj, **kwargs)
        disabled_fields = set()  # type: Set[str]

        # Validando os campos de acordo com as permissões
        if not request.user.has_perm('pode_ver_editar_tabela_conjugue'):
            raise Http404()

        return form


@admin.register(models.JuntaDiscipulado)
class JuntaDiscipuladoAdmin(admin.ModelAdmin):
    list_display = ('discipulador', 'discipulo')
    fields = ('discipulador', 'discipulo')
    list_display_links = ('discipulador', 'discipulo')
    search_fields = ('discipulador', 'discipulo')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Apresentando as informações de acordo com o tipo de usuario
        if request.user.has_perm('pode_ver_editar_tabela_junta_discipulado'):
            return qs.all()
        else:
            raise Http404()

    def get_form(self, request, obj=None, **kwargs):
        # Formulário para editar pessoas
        qs = super().get_queryset(request)
        form = super().get_form(request, obj, **kwargs)
        disabled_fields = set()  # type: Set[str]

        # Validando os campos de acordo com as permissões
        if not request.user.has_perm('pode_ver_editar_tabela_junta_discipulado'):
            raise Http404()

        return form


@admin.register(models.Telefone)
class TelefoneAdmin(admin.ModelAdmin):
    list_display = ('pessoa', 'numero', 'descricao')
    fields = ('pessoa', 'numero', 'esposa')
    list_display_links = ('pessoa', 'numero', 'descricao')
    search_fields = ('pessoa', 'numero', 'descricao')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Apresentando as informações de acordo com o tipo de usuario
        if request.user.has_perm('pode_ver_editar_tabela_telefone'):
            return qs.all()
        else:
            raise Http404()

    def get_form(self, request, obj=None, **kwargs):
        # Formulário para editar pessoas
        qs = super().get_queryset(request)
        form = super().get_form(request, obj, **kwargs)
        disabled_fields = set()  # type: Set[str]

        # Validando os campos de acordo com as permissões
        if not request.user.has_perm('pode_ver_editar_tabela_telefone'):
            raise Http404()

        return form
