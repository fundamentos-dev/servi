#from types import NoneType
import re

from app.core import models
from django.contrib import admin
from django.core.exceptions import PermissionDenied, ValidationError
from django.forms import ModelForm
from django.http import Http404


@admin.register(models.Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'nome', 'data_nascimento', 'discipulo_vinculado', 'apelido', 'data_vinculacao_igreja_local', \
                    'data_afastamento', 'sexo')
    fields = ('email', 'nome', 'apelido', 'data_vinculacao_igreja_local', \
                    'data_afastamento', 'sexo', 'estado_civil', 'grupo_caseiro')
    list_display_links = ('id', 'email', 'nome')
    search_fields = ('nome', 'email')
    
    
    #def __init__(self, *args, **kwargs):


    def get_queryset(self, request):
        qs = super().get_queryset(request)

        ## Testando qual tipo de permissão tem o usuário
        request_discipulo = request.user.has_perm('pode_ver_editar_proprios_dados')
        request_lider_g_caseiro = request.user.has_perm('pode_ver_discipulos_grupo_caseiro')
        request_auxiliar_diacono = request.user.has_perm('pode_ver_editar_discipulos_grupo_caseiro')
        request_diacono_bloco = request.user.has_perm('pode_ver_proprio_bloco')
        request_diacono_bloco_geral = request.user.has_perm('pode_editar_proprio_bloco')
        request_presbitero_diacono_geral = request.user.has_perm('pode_ver_dados_toda_igreja')

        ## Apresentando as informações de acordo com o tipo de usuario
        if request_discipulo and not request.user.is_superuser:
            return qs.filter(email = request.user.email)
        elif request_lider_g_caseiro and request_auxiliar_diacono and not request.user.is_superuser:
            return qs.filter(grupo_caseiro = request.user.grupo_caseiro)
        elif request_diacono_bloco and not request.user.is_superuser:
            return qs.filter(grupo_caseiro__bloco_id = request.user.grupo_caseiro.bloco.id)
        return qs.all()
    
    
    def get_form(self, request, obj=None, **kwargs):
        ## Formulário para editar pessoas
        qs = super().get_queryset(request)
        form = super().get_form(request, obj, **kwargs)
        disabled_fields = set()  # type: Set[str]
        
        ## Validando os campos de acordo com as permissões
        if request.user.has_perm('pode_ver_editar_proprios_dados') and not request.user.is_superuser:
            if not 'pai' in self.fields:
                self.fields = self.fields + ('pai', 'mae')
            disabled_fields |= {
                'nivel',
                'funcao',
                'grupo_caseiro',
                'data_afastamento',
                'motivo_afastamento',
                'data_vinculacao_igreja_local',  
            }
        elif request.user.has_perm('pode_ver_discipulos_grupo_caseiro') and request.user.has_perm('nao_pode_editar') and not request.user.is_authenticated:
            raise PermissionDenied()
        elif request.user.has_perm('pode_editar_proprio_bloco'):
            filtro = list(qs.filter(grupo_caseiro__bloco_id = request.user.grupo_caseiro.bloco.id))
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
                raise PermissionDenied()

            
            
        ## Criando laço para pecorrer os campos desabiltados
        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form


@admin.register(models.MotivoAfastamento)
class MotivoAfastmentoAdmin(admin.ModelAdmin):
    pass


@admin.register(models.OrigemDiscipulo)
class OrigemDiscipuloAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Profissao)
class ProfissaoAdmin(admin.ModelAdmin):
    pass


@admin.register(models.EstadoCivil)
class EstadoCivilAdmin(admin.ModelAdmin):
    pass



@admin.register(models.Bloco)
class BlocoAdmin(admin.ModelAdmin):
    pass



@admin.register(models.GrupoCaseiro)
class IgrejaCasaAdmin(admin.ModelAdmin):
    pass



@admin.register(models.Localidade)
class LocalidadeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Funcao)
class FuncaoAdmin(admin.ModelAdmin):
    pass


@admin.register(models.NivelServico)
class NivelServicoAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Permissao)
class PermissaoAdmin(admin.ModelAdmin):
    pass


@admin.register(models.PessoaPermissao)
class PessoaPermissaoAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Conjugue)
class ConjugueAdmin(admin.ModelAdmin):
    pass

@admin.register(models.JuntaDiscipulado)
class JuntaDiscipuladoAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Telefone)
class TelefoneAdmin(admin.ModelAdmin):
    pass
