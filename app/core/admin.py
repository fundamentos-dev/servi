from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.http import Http404

from . import models


class AbcForm(ModelForm):
    class Meta:
        model = models.Pessoa
        exclude = ["nome", "email"]

@admin.register(models.Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'nome', 'data_nascimento', 'discipulo_vinculado', 'apelido', 'data_vinculacao_igreja_local', \
                    'data_afastamento', 'sexo')
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
        if request_discipulo:
            return qs.filter(email = request.user.email)
        elif request_lider_g_caseiro and request_auxiliar_diacono:
            return qs.filter(grupo_caseiro = request.user.grupo_caseiro)
        elif request_diacono_bloco and not request.user.is_superuser:
            return qs.filter(grupo_caseiro__bloco_id = request.user.grupo_caseiro.bloco.id)
        return qs.all()
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        disabled_fields = set()  # type: Set[str]

        if request.user.has_perm('pode_ver_editar_proprios_dados'):
            disabled_fields |= {
                'nivel',
                'funcao',
                'grupo_caseiro',
                'data_afastamento',
                'motivo_afastamento',
                'data_vinculacao_igreja_local',
                
            }
        elif request.user.has_perm('pode_editar_proprio_bloco'):
            disabled_fields |= {
                'grupo_caseiro',
            }
            

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
