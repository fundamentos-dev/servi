from time import clock_settime
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Pessoa


class Discipulo: 
    pass


class AuxiliarDiacono:
    pass


class LiderIgrejaCasa:
    pass


class DiaconoGeral:
    pass


class Presbiterio:
    new_group, created = Group.objects.get_or_create(name='Presbiterio')
    # Code to add permission to group ???
    ct = ContentType.objects.get_for_model(Pessoa)

    # Now what - Say I want to add 'Can add project' permission to new_group?
    permission = Permission.objects.create(codename='can_view_grupo_caseiro',
                                    name='Can add project',
                                    content_type=ct)
    new_group.permissions.add(permission)


class Administrador:
    pass