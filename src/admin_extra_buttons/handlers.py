from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any

from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseBase
from django.utils.functional import cached_property

from .buttons import Button, ChoiceButton, LinkButton
from .utils import (
    HttpResponseRedirectToReferrer,
    check_permission,
    handle_basic_auth,
    labelize,
)

if TYPE_CHECKING:
    from .types import HandlerFunction, PermissionHandler


class BaseExtraHandler:
    def __init__(self, func, **kwargs) -> None:
        self.func = func
        self.func.extra_buttons_handler = self
        self.config = kwargs
        self.model_admin = kwargs.get("model_admin")
        self.decorators = kwargs.get("decorators", [])
        self.login_required = kwargs.get("login_required", True)
        self._pattern = kwargs.get("pattern", "")
        self.permission: str | PermissionHandler | None = kwargs.get("permission")
        self._sig: inspect.Signature = inspect.signature(self.func)

    @cached_property
    def func_args(self) -> list[Any]:
        return list(self._sig.parameters)

    @cached_property
    def single_object_invocation(self) -> bool:
        return len(self.func_args) == 2  # noqa: PLR2004

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.name}>"

    def get_instance(self, model_admin):
        """return a 'clone' of current Handler"""
        return self.__class__(self.func, model_admin=model_admin, **self.config)

    @cached_property
    def name(self) -> str:
        return self.func.__name__

    def __call__(self, model_admin, request, *args, **kwargs):
        obj = None
        self.model_admin = model_admin
        if not self.single_object_invocation:
            pk = str(kwargs.get(self.func_args[2]))
            obj = model_admin.get_object(request, pk)

        if self.permission:
            check_permission(self, self.permission, request, obj)
        elif self.login_required and not request.user.is_authenticated:
            raise PermissionDenied

        ret = self.func(model_admin, request, *args, **kwargs)

        if not isinstance(ret, HttpResponseBase):
            return HttpResponseRedirectToReferrer(request)
        return ret


class ViewHandler(BaseExtraHandler):
    def __init__(
        self,
        func,
        login_required=True,
        http_basic_auth=False,
        http_auth_handler=None,
        **kwargs,
    ) -> None:
        self.login_required = login_required
        if http_auth_handler:
            if http_basic_auth:
                raise ValueError("'http_basic_auth' and 'http_auth_handler' are mutually exclusive")
            self.http_auth_handler = http_auth_handler
        else:
            self.http_basic_auth = http_basic_auth
            self.http_auth_handler = handle_basic_auth
        super().__init__(
            func,
            http_auth_handler=http_auth_handler,
            http_basic_auth=http_basic_auth,
            login_required=login_required,
            **kwargs,
        )

    def __call__(self, model_admin, request, *args, **kwargs):
        self.model_admin = model_admin
        if self.login_required and self.http_basic_auth and not request.user.is_authenticated:
            self.http_auth_handler(request)
        return super().__call__(model_admin, request, *args, **kwargs)

    @cached_property
    def url_pattern(self) -> str:
        if self._pattern:
            return self._pattern
        pattern = ""
        for arg in list(self.func_args)[2:]:
            pattern += f"<path:{arg}>/"
        pattern += f"{self.name}/"
        return pattern


class ButtonMixin:
    def __init__(
        self,
        func: "HandlerFunction",
        html_attrs: dict[str, str] | None = None,
        change_list: bool | None = None,
        change_form: bool | None = None,
        visible: bool = True,
        enabled: bool = True,
        **kwargs: Any,
    ) -> None:
        self.change_form = change_form
        self.change_list = change_list
        self.visible = visible
        self.enabled = enabled
        self.html_attrs = html_attrs or {}
        super().__init__(
            func,
            change_form=change_form,
            change_list=change_list,
            html_attrs=html_attrs,
            enabled=enabled,
            visible=visible,
            **kwargs,
        )

    def get_button_params(self, context, **extra):
        return {
            "label": self.config.get("label", labelize(self.name)),
            "handler": self,
            "html_attrs": self.html_attrs,
            "change_list": self.change_list,
            "change_form": self.change_form,
            "visible": self.visible,
            "enabled": self.enabled,
            "context": context,
            "login_required": self.login_required,
            "permission": self.permission,
            **extra,
        }

    def get_button(self, context):
        return self.button_class(**self.get_button_params(context))


class ButtonHandler(ButtonMixin, ViewHandler):
    """View handler for `@button` decorated views"""

    button_class = Button


class LinkHandler(ButtonMixin, BaseExtraHandler):
    button_class = LinkButton
    url_pattern = None

    def __init__(self, func, **kwargs) -> None:
        self.href = kwargs.pop("href", None)
        super().__init__(func, href=self.href, **kwargs)

    def get_button_params(self, context, **extra):
        return super().get_button_params(
            context,
            href=self.href,
            url_pattern=self.url_pattern,
            **extra,
        )

    def get_button(self, context):
        params = self.get_button_params(context)
        button = self.button_class(**params)
        self.func(self.model_admin, button)
        return button


class ChoiceHandler(LinkHandler):
    button_class = ChoiceButton

    def __init__(self, func, **kwargs) -> None:
        self.href = kwargs.pop("href", None)
        self.choices = kwargs.pop("choices", None)
        self.selected_choice = None
        super().__init__(func, href=self.href, choices=self.choices, **kwargs)

    def get_button_params(self, context, **extra):
        return super().get_button_params(
            context,
            choices=self.choices,
            **extra,
        )
