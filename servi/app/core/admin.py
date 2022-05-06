from django.contrib import admin
from . import models

@admin.register(models.Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'nome', 'data_nascimento', 'discipulo_vinculado', 'apelido', 'data_vinculacao_igreja_local', \
                    'data_afastamento', 'sexo')
    list_display_links = ('id', 'email', 'nome')
    search_fields = ('nome', 'email')


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
