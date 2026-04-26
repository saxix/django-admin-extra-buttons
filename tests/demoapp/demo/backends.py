from typing import TYPE_CHECKING, Any

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.http import HttpRequest

if TYPE_CHECKING:
    from django.contrib.auth.models import AnonymousUser


class AnyUserBackend(ModelBackend):
    def user_can_authenticate(self, user: Any) -> bool:
        return True

    def has_perm(self, user_obj: User | "AnonymousUser", perm: str, obj: Any = None) -> bool:
        return True

    def has_module_perms(self, user_obj: User | "AnonymousUser", app_label: str) -> bool:
        return True

    def authenticate(
        self,
        request: HttpRequest | None,
        username: str | None = None,
        password: str | None = None,
        **kwargs: Any,
    ) -> User | None:
        u, __ = User.objects.update_or_create(
            username=username,
            defaults={"email": username, "is_active": True, "is_staff": True, "is_superuser": True},
        )
        return u
