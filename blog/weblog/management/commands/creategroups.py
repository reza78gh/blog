from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = "create groups and permissions for writer, editor and manager"

    def handle(self, *args, **options):
        can_write = Permission.objects.get(codename='can_write')
        can_edit = Permission.objects.get(codename='can_edit')
        can_manage = Permission.objects.get(codename='can_manage')
        new_group, _=Group.objects.get_or_create(name='نویسنده')
        new_group.permissions.add(can_write)
        new_group, _=Group.objects.get_or_create(name='ویراستار')
        new_group.permissions.add(can_write,can_edit)
        new_group, _=Group.objects.get_or_create(name='مدیر')
        new_group.permissions.add(can_write,can_edit,can_manage)
        self.stdout.write(self.style.SUCCESS('Groups created successfully'))
