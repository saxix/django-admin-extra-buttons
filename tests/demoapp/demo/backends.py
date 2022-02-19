from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class AnyUserBackend(ModelBackend):

    def user_can_authenticate(self, a):
        return True

    def has_perm(self, user_obj, perm, obj=None):
        return True

    def has_module_perms(self, user_obj, app_label):
        return True

    def authenticate(self, request, username=None, password=None, **kwargs):
        u, __ = User.objects.update_or_create(
            username=username,
            defaults={"email": username, "is_active": True, "is_staff": True, "is_superuser": True},
        )
        return u
