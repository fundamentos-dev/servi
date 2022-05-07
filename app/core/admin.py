from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Pessoa, Bloco


@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'nome', 'data_nascimento', 'discipulo_vinculado', 'apelido', 'data_vinculacao_igreja_local', \
                    'data_afastamento', 'sexo')
    list_display_links = ('id', 'email', 'nome')
    search_fields = ('nome', 'email')
    
   
    # def add_view(self, request, form_url = '', extra_context = None):
    #     try:
    #         return super(models.Pessoa, self).add_view(
    #             request, form_url, extra_context
    #         )
    #     except ValidationError as e:
    #         print(e)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # if request.user.is_superuser:
        #     return qs.all()
        
        ## Testando qual tipo de permissão tem o usuário
        request_discipulo = request.user.has_perm('pode_ver_editar_proprios_dados')
        request_lider_g_caseiro = request.user.has_perm('pode_ver_discipulos_grupo_caseiro')
        request_auxiliar_diacono = request.user.has_perm('pode_ver_editar_discipulos_grupo_caseiro')
        
        ## Apresentando as informações de acordo com o tipo de usuario
        if request_discipulo and not request.user.is_superuser:
            return qs.filter(email = request.user.email)
        elif request_lider_g_caseiro or request_auxiliar_diacono :
            return qs.filter(grupo_caseiro = request.user.grupo_caseiro)
      
        return True
    

# @admin.register(models.MotivoAfastmento)
# class MotivoAfastmentoAdmin(admin.ModelAdmin):
#     pass


# @admin.register(models.OrigemDiscipulo)
# class OrigemDiscipuloAdmin(admin.ModelAdmin):
#     pass


# @admin.register(models.Profissao)
# class ProfissaoAdmin(admin.ModelAdmin):
#     pass


# @admin.register(models.EstadoCivil)
# class EstadoCivilAdmin(admin.ModelAdmin):
#     pass



# @admin.register(models.Bloco)
# class BlocoAdmin(admin.ModelAdmin):
#     pass



# @admin.register(models.GrupoCaseiro)
# class IgrejaCasaAdmin(admin.ModelAdmin):
#     pass



# @admin.register(models.Localidade)
# class LocalidadeAdmin(admin.ModelAdmin):
#     pass


# @admin.register(models.Funcao)
# class FuncaoAdmin(admin.ModelAdmin):
#     pass


# @admin.register(models.NivelServico)
# class NivelServicoAdmin(admin.ModelAdmin):
#     pass


# @admin.register(models.Permissao)
# class PermissaoAdmin(admin.ModelAdmin):
#     pass


# @admin.register(models.PessoaPermissao)
# class PessoaPermissaoAdmin(admin.ModelAdmin):
#     pass


# @admin.register(models.Conjugue)
# class ConjugueAdmin(admin.ModelAdmin):
#     pass


# @admin.register(models.JuntaCompanheirismo)
# class JuntaCompanheirismoAdmin(admin.ModelAdmin):
#     pass


# @admin.register(models.JuntaDiscipulado)
# class JuntaDiscipuladoAdmin(admin.ModelAdmin):
#     pass


# @admin.register(models.Telefone)
# class TelefoneAdmin(admin.ModelAdmin):
#     pass
