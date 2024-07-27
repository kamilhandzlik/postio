from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from .models import UserPackage


@receiver(post_migrate)
def create_supplier_group(sender, **kwargs):
    if sender.name == 'main':
        group, created = Group.objects.get_or_create(name="Dostawca")
        if created:
            content_type = ContentType.objects.get_for_model(UserPackage)
            permissions = Permission.objects.filter(content_type=content_type).exclude(
                codename__in=['delete_userpackage'])
            group.permissions.set(permissions)
