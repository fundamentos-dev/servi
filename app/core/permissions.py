from .models1 import IgrejaCasa, Pessoa
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class AuxiliarDiacono(Permission, ContentType):
    if Pessoa.funcao == 'auxiliar_diacono':
        content_type = ContentType.objects.get_for_model(Pessoa)
        permission = Permission.objects.create(
            if Pessoa.IgrejaCasa == self.IgrejaCasa:
            codename='can_view',
            name='Can Publish Posts',
            content_type=content_type,
        )