from __future__ import annotations

import copy
import inspect
from typing import TYPE_CHECKING, Any

from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseBase
from django.utils.functional import cached_property
from django.contrib import admin

from .buttons import ButtonWidget, ChoiceButton, LinkButton
from .utils import HttpResponseRedirectToReferrer, check_permission, handle_basic_auth, labelize

if TYPE_CHECKING:
    from collections.abc import Callable

    from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
    from django.http import HttpRequest
    from django.template import RequestContext

    from .mixins import ExtraButtonsMixin
    from .types import HandlerFunction, PermissionHandler, VisibleButton


class ButtonHandler:
    """
    A descriptor and handler for admin buttons.

    It stores button configuration and creates a unique instance for each
    ModelAdmin instance to which it is attached.
    """

    def __init__(
        self,
        func: Callable,
        html_attrs: dict[str, Any] | None = None,
        change_list: bool | None = None,
        change_form: bool | None = None,
    ):
        self.func = func
        self.html_attrs = html_attrs or {}
        self.change_list = change_list
        self.change_form = change_form

        # These will be populated by the mixin
        self.model_admin: admin.ModelAdmin | None = None
        self.method_name: str = ""
        self.url_name: str = ""

        # Compatibility with original function attributes
        for attr in ["__name__", "__doc__", "__module__", "__qualname__"]:
            if hasattr(func, attr):
                setattr(self, attr, getattr(func, attr))

    def get_instance(self, model_admin: admin.ModelAdmin) -> "ButtonHandler":
        """
        Return a new instance of the handler bound to the ModelAdmin instance.
        """
        instance = copy.copy(self)
        instance.model_admin = model_admin
        return instance

    def __call__(self, request: Any, *args: Any, **kwargs: Any) -> Any:
        """
        Call the original decorated function, passing the model_admin instance.
        """
        if not self.model_admin:
            # This should not happen in the context of a ModelAdmin
            raise TypeError(
                "Button handler is not bound to a ModelAdmin instance."
            )
        return self.func(self.model_admin, request, *args, **kwargs)


class BaseExtraHandler:
    def __init__(self, func: HandlerFunction, **kwargs: Any) -> None:
        self.func: HandlerFunction = func
        self.func.extra_buttons_handler = self
        self.url_name: str = ""
        self.config = kwargs
        self.model_admin: "ExtraButtonsMixin" = kwargs.get("model_admin")  # type:ignore[assignment]
        self.decorators = kwargs.get("decorators", [])
        self.login_required = kwargs.get("login_required", True)
        self._pattern = kwargs.get("pattern", "") or ""
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

    def get_instance(self, model_admin: "ExtraButtonsMixin") -> "BaseExtraHandler":
        """return a 'clone' of current Handler"""
        return self.__class__(self.func, model_admin=model_admin, **self.config)

    @cached_property
    def name(self) -> str:
        return self.func.__name__

    def __call__(
        self, model_admin: "ExtraButtonsMixin", request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponseBase:
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
        func: "HandlerFunction",
        http_basic_auth: bool = False,
        http_auth_handler: Callable[[HttpRequest], AbstractBaseUser | AnonymousUser | None] | None = None,
        **kwargs: Any,
    ) -> None:
        if http_auth_handler:
            if http_basic_auth:
                raise ValueError("'http_basic_auth' and 'http_auth_handler' are mutually exclusive")
            self.http_auth_handler = http_auth_handler
            self.http_basic_auth = True
        else:
            self.http_basic_auth = http_basic_auth
            self.http_auth_handler = handle_basic_auth
        super().__init__(func, **kwargs)

    def __call__(
        self, model_admin: "ExtraButtonsMixin", request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponseBase:
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
    button_class: "type[VisibleButton]" = ButtonWidget

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
        self.config = kwargs
        self.change_form = change_form
        self.change_list = change_list
        self.visible = visible
        self.enabled = enabled
        self.html_attrs = html_attrs or {}

        super().__init__(  # type:ignore[call-arg]
            func,
            change_form=change_form,
            change_list=change_list,
            html_attrs=html_attrs,
            enabled=enabled,
            visible=visible,
            **kwargs,
        )

    def get_button_params(self, context: "RequestContext", **extra: Any) -> dict[str, Any]:
        return {
            "handler": self,
            "html_attrs": self.html_attrs,
            "change_list": self.change_list,
            "change_form": self.change_form,
            "visible": self.visible,
            "enabled": self.enabled,
            "context": context,
            **extra,
        }

    def get_button(self, context: "RequestContext") -> "ButtonWidget":
        return self.button_class(**self.get_button_params(context))


class LinkHandler(ButtonMixin, BaseExtraHandler):
    button_class: "type[VisibleButton]" = LinkButton
    url_pattern = None

    def __init__(self, func: HandlerFunction, **kwargs: Any) -> None:
        self.href = kwargs.pop("href", None)
        self.label = kwargs.get("label")
        super().__init__(func, href=self.href, **kwargs)

    def get_button_params(self, context: RequestContext, **extra: Any) -> dict[str, Any]:
        return super().get_button_params(
            context,
            href=self.href,
            label=self.label,
            url_pattern=self.url_pattern,
            **extra,
        )

    def get_button(self, context: "RequestContext") -> "ButtonWidget":
        params = self.get_button_params(context)
        button = self.button_class(**params)
        if not button.label:
            button.label = self.func.__name__
        self.func(self.model_admin, button)
        return button


class ChoiceHandler(LinkHandler):
    button_class: "type[VisibleButton]" = ChoiceButton

    def __init__(self, func: "HandlerFunction", **kwargs: Any) -> None:
        self.href = kwargs.pop("href", None)
        self.choices = kwargs.pop("choices", None)
        self.label = kwargs.get("label")
        self.selected_choice = None
        super().__init__(func, href=self.href, choices=self.choices, **kwargs)

    def get_button_params(self, context: RequestContext, **extra: Any) -> dict[str, Any]:
        return super().get_button_params(
            context,
            choices=self.choices,
            **extra,
        )


__all__ = ["ButtonHandler"]
