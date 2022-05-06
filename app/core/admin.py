from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

from . import models
from .models import Pessoa


@admin.register(models.Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'nome', 'data_nascimento', 'discipulo_vinculado', 'apelido', 'data_vinculacao_igreja_local', \
                    'data_afastamento', 'sexo')
    list_display_links = ('id', 'email', 'nome')
    search_fields = ('nome', 'email')
    
    ct = ContentType.objects.get_for_model(Pessoa)
    pm = Permission.objects.get_or_create(codename='can_view_self_data',
                                    name='Pode ver os próprios dados',
                                    content_type=ct)
    grupo_discipulo = Group.objects.get_or_create(name='Auxiliar Diácono')
    #grupo_discipulo.permissions.add(pm)    
    
    def add_view(self, request, form_url='', extra_context=None):
        try:
            return super(models.Pessoa, self).add_view(
                request, form_url, extra_context
            )
        except ValidationError as e:
            print(e)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.has_perm('can_view_self_data'):
            return qs.filter(email=request.user.email)
        else:
            pass
        # Filtrar apenas que ainda não tenham sido revisadas
        raise Http404

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "criado_por":
    #         kwargs["initial"] = request.user.id
    #         kwargs["disabled"] = True
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # def change_view(self, request, object_id, extra_context=None):
    #     if request.user.has_perm('can_view_self_data'):
    #         self.fields.append('nome')
    #         self.fields.append('senha')
    #         self.readonly_fields.append('data_nascimento')
    #         self.readonly_fields.append('email')
    #     if request.user.has_perm('publish_question'):
    #         self.fields.append('publicado_por')
    #         self.fields.append('publicado_em')
    #         # self.readonly_fields = ('revisado_por','revisado_em')

    # def save_model(self, request, obj, form, change):
    #     # Se quem salvou é PUBLICADOR, então ele ganha o publicado_em e publicado_por
    #     obj.user = request.user
    #     super().save_model(request, obj, form, change)
    
    


@admin.register(models.MotivoAfastmento)
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



@admin.register(models.IgrejaCasa)
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


@admin.register(models.JuntaCompanheirismo)
class JuntaCompanheirismoAdmin(admin.ModelAdmin):
    pass


@admin.register(models.JuntaDiscipulado)
class JuntaDiscipuladoAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Telefone)
class TelefoneAdmin(admin.ModelAdmin):
    pass
