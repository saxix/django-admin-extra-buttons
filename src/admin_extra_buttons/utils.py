from __future__ import annotations

import ast
import codecs
import inspect
from typing import TYPE_CHECKING, Any
from urllib.parse import urlencode

from django.conf import settings
from django.core import checks
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponseRedirect

if TYPE_CHECKING:
    from _ast import FunctionDef

    from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
    from django.db.models import Model

    from .handlers import BaseExtraHandler
    from .mixins import ExtraButtonsMixin
    from .types import PermissionHandler


def handle_basic_auth(request: HttpRequest) -> "AbstractBaseUser | AnonymousUser | None":
    from django.contrib.auth import authenticate, login  # noqa: PLC0415

    if "HTTP_AUTHORIZATION" in request.META:
        authmeth, auth = request.META["HTTP_AUTHORIZATION"].split(" ", 1)
        if authmeth.lower() == "basic":
            auth = codecs.decode(auth.encode("utf8").strip(), "base64").decode()
            username, password = auth.split(":", 1)
            user = authenticate(request=request, username=username, password=password)
            if user:  # pragma: no branch
                login(request, user)
                return user
    raise PermissionDenied


def get_preserved_filters(request: HttpRequest) -> str:
    filters = request.GET.get("_changelist_filters", "")
    preserved_filters = request.GET.get("_changelist_filters") if filters else request.GET.urlencode()

    if preserved_filters:
        return urlencode({"_changelist_filters": preserved_filters})
    return ""


def labelize(label: str) -> str:
    return label.replace("_", " ").strip().title()


def check_permission(
    handler: "BaseExtraHandler",
    permission: "str|PermissionHandler",
    request: HttpRequest,
    obj: Model | None = None,
) -> bool:
    if callable(permission):
        if not permission(request, obj, handler=handler):
            raise PermissionDenied
    elif not request.user.has_perm(permission):
        raise PermissionDenied
    return True


class HttpResponseRedirectToReferrer(HttpResponseRedirect):
    def __init__(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        redirect_to = request.META.get("HTTP_REFERER", "/")
        super().__init__(redirect_to, *args, **kwargs)


def get_all_permissions() -> list[str]:
    from django.contrib.auth.models import Permission  # noqa: PLC0415

    return [
        f"{p[0]}.{p[1]}"
        for p in (Permission.objects.select_related("content_type").values_list("content_type__app_label", "codename"))
    ]


def check_decorator_errors(model_admin: "ExtraButtonsMixin") -> list[checks.Warning]:
    target = type(model_admin)
    standard_permissions = []
    errors = []
    if "django.contrib.auth" in settings.INSTALLED_APPS:  # pragma: no branch
        standard_permissions = get_all_permissions()

    def visit_function_dev(node: "FunctionDef") -> None:
        for n in node.decorator_list:
            if isinstance(n, ast.Call):
                name = n.func.attr if isinstance(n.func, ast.Attribute) else n.func.id  # type:ignore[attr-defined]
            else:
                name = n.attr if isinstance(n, ast.Attribute) else n.id  # type:ignore[attr-defined]
            if name in {"button", "view"} and standard_permissions:  # pragma: no branch
                for k in n.keywords:  # type:ignore[attr-defined]
                    if k.arg == "permission" and isinstance(k.value, ast.Constant):
                        perm_name = k.value.value
                        if perm_name not in standard_permissions:
                            errors.append(
                                checks.Warning(
                                    f'"{target.__name__}.{node.name}" '
                                    f"is checking for a non existing permission "
                                    f'"{perm_name}"',
                                    id="admin_extra_buttons.PERM",
                                )
                            )

    node_iter = ast.NodeVisitor()
    node_iter.visit_FunctionDef = visit_function_dev  # type:ignore[method-assign]
    node_iter.visit(ast.parse(inspect.getsource(target)))
    return errors
