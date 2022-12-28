#from types import NoneType
from pprint import pprint
import re
from wsgiref.util import request_uri
from app.core import models
from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from more_admin_filters import MultiSelectRelatedFilter
import csv
from django.http import HttpResponse
from django.db.models import Q

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
    list_display = ('id', 'discipulo_vinculado', 'email', 'nome', 'username', 'data_nascimento', 'apelido', 'sexo', 'grupo_caseiro', 'estado_civil', 'conjuge', 'pai', 'mae', 'data_vinculacao_igreja_local',
                    'origem', 'nivel_servico', 'funcao', 'profissao', 'localidade', 'data_afastamento', 'motivo_afastamento')
    fields = ['nome', 'username', 'data_nascimento', 'apelido', 'sexo', 'email', 'discipulo_vinculado', 'grupo_caseiro', 'discipuladores', 'companheiros', 'estado_civil', 'conjuge', 'pai', 'mae', 'data_vinculacao_igreja_local',
              'origem', 'nivel_servico', 'funcao', 'profissao', 'localidade', 'data_afastamento', 'motivo_afastamento']
    list_display_links = ('id', 'email', 'nome')
    search_fields = ('nome', 'email')
    readonly_fields = ('username', )
    # https://github.com/thomst/django-more-admin-filters
    list_filter = [('estado_civil', MultiSelectRelatedFilter),
                   ('nivel_servico', MultiSelectRelatedFilter), 'grupo_caseiro']
    raw_id_fields = ['mae', 'pai', 'companheiros', 'conjuge', 'discipuladores']
    autocomplete_fields = ['pai', 'mae']
    list_per_page = 25
    inlines = [
        TelefoneInline
    ]

    actions = ['download_csv']

    def download_csv(self, request, queryset):
        with open('relatorio.csv', 'wt') as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(['id', 'email', 'nome', 'data_nascimento', 'apelido', 'discipulo_vinculado', 'data_vinculacao_igreja_local',
                             'data_afastamento', 'sexo', 'funcao', 'estado_civil', 'grupo_caseiro', 'localidade', 'nivel_servico', 'origem', 'profissao', 'pai', 'mae', 'conjuge'])
            for dado in queryset:
                writer.writerow([dado.id, dado.email, dado.nome, dado.data_nascimento, dado.apelido, dado.discipulo_vinculado, dado.data_vinculacao_igreja_local, dado.data_afastamento,
                                dado.sexo, dado.funcao, dado.estado_civil, dado.grupo_caseiro, dado.localidade, dado.nivel_servico, dado.origem, dado.profissao, dado.pai, dado.mae, dado.conjuge])

        with open('relatorio.csv', 'r') as arquivo:
            response = HttpResponse(arquivo, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=relatorio.csv'
            return response
    download_csv.short_description = "Download CSV."

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "funcao" and request.user.funcao is not None:
            # Podem mostrar apenas as funções de ids iguais ou inferiores
            kwargs["queryset"] = models.Funcao.objects.filter(id__lte=request.user.funcao.id)
        elif db_field.name == "nivel_servico" and request.user.nivel_servico is not None:
            # Podem mostrar apenas as funções de ids iguais ou inferiores
            kwargs["queryset"] = models.Funcao.objects.filter(id__lte=request.user.nivel_servico.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Criando regras para visualização de registro de acordo com as permissões
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # qs = qs.filter(discipulo_vinculado=True)
        # Apresentando as informações de acordo com o tipo de usuário        
        if request.user.has_perm('core.view_self_pessoa') and not request.user.is_superuser:
            # Só visualiza a si próprio
            return qs.filter(email=request.user.email)
        elif request.user.has_perm('core.view_grupocaseiro_pessoa') and not request.user.is_superuser:
            # Deve mostrar os dados do grupo caseiro e todos os relacionados por juntas naturais, companheirismo ou discipulador
            return qs.filter(Q(grupo_caseiro=request.user.grupo_caseiro) | Q(discipuladores__grupo_caseiro=request.user.grupo_caseiro) | Q(companheiros__grupo_caseiro=request.user.grupo_caseiro) | Q(pessoa_pai__grupo_caseiro=request.user.grupo_caseiro) | Q(pessoa_mae__grupo_caseiro=request.user.grupo_caseiro))
        elif request.user.has_perm('core.view_grupocaseiro_bloco_pessoa') and not request.user.is_superuser:
            # Visualiza todos os do bloco e vinculados
            return qs.filter(Q(grupo_caseiro__bloco_id=request.user.grupo_caseiro.bloco.id) | Q(discipuladores__grupo_caseiro__bloco_id=request.user.grupo_caseiro.bloco.id) | Q(companheiros__grupo_caseiro__bloco_id=request.user.grupo_caseiro.bloco.id) | Q(pessoa_pai__grupo_caseiro__bloco_id=request.user.grupo_caseiro.bloco.id) | Q(pessoa_mae__grupo_caseiro__bloco_id=request.user.grupo_caseiro.bloco.id))
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
            if obj.funcao.id == 1:
                g_auxiliar_diacono.user_set.add(obj)
            elif obj.funcao.id == 2:
                g_diacono_bloco.user_set.add(obj)
            elif obj.funcao.id == 3:
                g_diacono_geral.user_set.add(obj)
            elif obj.funcao.id == 5:
                g_administrador.user_set.add(obj)
        elif obj.discipulo_vinculado:
            g_discipulo.user_set.add(obj)

        if obj.discipulo_vinculado:
            obj.is_staff = True

        if obj.data_afastamento is not None:
            obj.discipulo_vinculado = False
            obj.is_staff = False
            obj.is_active = False

    # Criando regras para edição de regristros de acordo com as permissões
    def get_form(self, request, obj=None, **kwargs):
        # Formulário para editar pessoas
        qs = super().get_queryset(request)
        # form = super().get_form(request, obj, **kwargs)
        current_user = request.user
        fields_to_disable = []

        permissions = [{'codename': p.codename}
                       for p in Permission.objects.filter(group__user=request.user).all()]
        # pprint(permissions)
        
        # Variável que determina se o formulário é mostrado ou não
        controle = False
        # Validando os campos de acordo com as permissões
        if request.user.has_perm('core.cannot_change_funcao_pessoa') and not request.user.is_superuser:
            # Usuário é um discipulo que não pode editar sua própria função nem ver alguns de seus campos
            fields_to_disable = [
                'username', 'pai', 'mae', 'funcao', 'grupo_caseiro'
            ]

        elif request.user.has_perm('core.change_grupocaseiro_pessoa') and not request.user.is_superuser:
            # Não é superusuário, mas tem permissão de mudar pessoas que sejam do mesmo grupo caseiro
            if request.user.grupo_caseiro:
                filtro = list(
                    qs.filter(Q(grupo_caseiro=request.user.grupo_caseiro) | Q(discipuladores__grupo_caseiro=request.user.grupo_caseiro) | Q(companheiros__grupo_caseiro=request.user.grupo_caseiro) | Q(pessoa_pai__grupo_caseiro=request.user.grupo_caseiro) | Q(pessoa_mae__grupo_caseiro=request.user.grupo_caseiro)))
                # Capturando toda a url da requisição
                url = str(request.get_full_path)
                if re.sub('[^0-9]', '', url):
                    # Verifica o id da pessoa a ser editada que fica armazenada na url
                    id_form = int(re.sub('[^0-9]', '', url))
                    for pessoa in filtro:
                        id = pessoa.id
                        if id_form == id:
                            controle = True
                    if not controle:
                        raise ValueError(
                            'Não tem autorização para acessar a página')

        elif request.user.has_perm('core.change_grupocaseiro_bloco_pessoa') and not request.user.is_superuser:
            if request.user.grupo_caseiro.bloco.id:
                filtro = list(
                    qs.filter(grupo_caseiro__bloco_id=request.user.grupo_caseiro.bloco.id))
                # Capturando toda a url da requisição
                url = str(request.get_full_path)
                if re.sub('[^0-9]', '', url):
                    # Verifica o id da pessoa a ser editada que fica armazenada na url
                    id_form = int(re.sub('[^0-9]', '', url))
                    for pessoa in filtro:
                        id = pessoa.id
                        if id_form == id:
                            controle = True
                    if not controle:
                        raise ValueError(
                            'Não tem autorização para acessar a página')

        form = super(PessoaAdmin, self).get_form(request, obj, **kwargs)
        form.current_user = current_user

        # Verifica se o usuário tem uma função inferior à do usuário a ser editado, se tiver desabilita o campo de função
        if obj is not None and (current_user.funcao is not None and obj.funcao is not None and current_user.funcao.id < obj.funcao.id) or current_user.funcao is None:
            fields_to_disable.append('funcao')
        # Verifica se o usuário tem uma nível de serviço inferior à do usuário a ser editado, se tiver desabilita o campo de nível de serviço
        if obj is not None and (current_user.nivel_servico is not None and obj.nivel_servico is not None and current_user.nivel_servico.id < obj.nivel_servico.id) or current_user.nivel_servico is None:
            fields_to_disable.append('nivel_servico')

        # Criando loop para pecorrer os campos desabiltados
        for f in fields_to_disable:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form

    def get_fields(self, request, obj=None):
        fields = super(PessoaAdmin, self).get_fields(request, obj)

        fields_to_remove = []
        if request.user.has_perm('core.cannot_change_funcao_pessoa') and not request.user.is_superuser:
            fields_to_remove = ['motivo_afastamento','data_afastamento', 'origem', 'nivel_servico']
            self.readonly_fields = ('data_vinculacao', 'companheiros', 'discipuladores', 'conjuge')

        # Criando loop para pecorrer os campos a ser removidos do form
        for f in fields_to_remove:
            if f in fields:
                fields.remove(f)

        return fields

    def save_form(self, request, form, change):
        if not change:
            discipuladores = form.cleaned_data.pop('discipuladores')
            companheiros = form.cleaned_data.pop('companheiros')
            for key, value in form.cleaned_data.items():
                print(key, value, type(value))
            form.instance = self.model.objects.create_user(
                **form.cleaned_data)
            form.instance.discipuladores.set(discipuladores)
            form.instance.companheiros.set(companheiros)
                
        return super().save_form(request, form, change)


# admin.site.register(models.Filho)
admin.site.register(models.MotivoAfastamento)
admin.site.register(models.OrigemDiscipulo)
admin.site.register(models.Profissao)
admin.site.register(models.EstadoCivil)
admin.site.register(models.Funcao)
admin.site.register(models.GrupoCaseiro)
admin.site.register(models.Bloco)
admin.site.register(models.Localidade)
admin.site.register(models.NivelServico)
admin.site.register(models.Telefone)
