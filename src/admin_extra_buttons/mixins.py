from __future__ import annotations

import inspect
import logging
from functools import partial
from typing import TYPE_CHECKING, Any

from django import forms
from django.conf import settings
from django.contrib import admin, messages
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.core.exceptions import ImproperlyConfigured
from django.db import OperationalError, ProgrammingError
from django.db.models import Model
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import URLPattern, path, reverse
from django.utils.safestring import SafeString

from .handlers import BaseExtraHandler, ButtonHandler, ChoiceHandler, LinkHandler, ViewHandler

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

    from django.contrib.admin import AdminSite
    from django.core.checks import CheckMessage
    from django.db.models.options import Options
    from django.template import RequestContext

    from .types import HandlerWithButton

logger = logging.getLogger(__name__)

IS_GRAPPELLI_INSTALLED = "grappelli" in settings.INSTALLED_APPS

NOTSET = object()


class ActionFailedError(Exception):
    pass


def confirm_action(  # noqa: PLR0913
    modeladmin: "ExtraButtonsMixin",
    request: HttpRequest,
    action: "Callable[..., HttpResponse | None]",
    *,
    message: str,
    success_message: str = "",
    description: str = "",
    pk: str | None = None,
    extra_context: dict[str, Any] | None = None,
    title: str | None = None,
    template: str = "admin_extra_buttons/confirm.html",
    error_message: str | None = None,
    raise_exception: bool = False,
) -> HttpResponse | None:
    opts: Options[Model] = modeladmin.model._meta
    if extra_context:
        title = extra_context.pop("title", title)
    context = modeladmin.get_common_context(
        request, message=message, description=description, title=title, pk=pk, **(extra_context or {})
    )
    if request.method == "POST":
        ret = None
        try:
            ret = action(request)
            if success_message:
                modeladmin.message_user(request, success_message, messages.SUCCESS)
        except Exception as e:  # pragma: no cover
            if raise_exception:
                raise
            if error_message:
                modeladmin.message_user(request, error_message or str(e), messages.ERROR)
        if ret:
            return ret
        return HttpResponseRedirect(reverse(admin_urlname(opts, SafeString("changelist"))))

    return TemplateResponse(request, template, context)


class ExtraUrlConfigError(RuntimeError):
    pass


class DummyAdminform:
    def __init__(self, **kwargs: Any) -> None:
        self.prepopulated_fields: list[str] = []
        self.__dict__.update(**kwargs)

    def __iter__(self) -> "Iterator[Any]":  # pragma: no cover
        yield


class ExtraButtonsMixin(admin.ModelAdmin[Model]):
    if IS_GRAPPELLI_INSTALLED:  # pragma: no cover
        change_list_template = "admin_extra_buttons/grappelli/change_list.html"
        change_form_template = "admin_extra_buttons/grappelli/change_form.html"
    else:
        change_list_template = "admin_extra_buttons/change_list.html"
        change_form_template = "admin_extra_buttons/change_form.html"

    def __init__(self, model: type[Model], admin_site: AdminSite) -> None:
        self.extra_button_handlers: "dict[str, HandlerWithButton]" = {}
        super().__init__(model, admin_site)

    def message_error_to_user(self, request: HttpRequest, exception: Exception) -> None:
        self.message_user(request, f"{exception.__class__.__name__}: {exception}", messages.ERROR)

    def check(self, **kwargs: Any) -> list[CheckMessage]:
        errors = super().check(**kwargs)
        try:
            from admin_extra_buttons.utils import check_decorator_errors  # noqa: PLC0415

            errors.extend(check_decorator_errors(self))
        except (OSError, OperationalError, ProgrammingError, ImproperlyConfigured):  # pragma: no cover
            pass
        return errors

    def get_common_context(self, request: HttpRequest, pk: str | None = None, **kwargs: Any) -> dict[str, Any]:
        opts = self.model._meta
        app_label = opts.app_label
        self.object = None
        if pk:
            self.object = self.get_object(request, pk)

        context = {
            **self.admin_site.each_context(request),
            **kwargs,
            "opts": opts,
            "add": False,
            "change": True,
            "save_as": False,
            "original": self.object,
            "extra_buttons": self.extra_button_handlers,
            "has_editable_inline_admin_formsets": False,
            "has_delete_permission": self.has_delete_permission(request, self.object),
            "has_view_permission": self.has_view_permission(request, self.object),
            "has_change_permission": self.has_change_permission(request, self.object),
            "has_add_permission": self.has_add_permission(request),
            "app_label": app_label,
            "adminform": DummyAdminform(model_admin=self),
        }
        context.setdefault("title", "")
        context.update(**kwargs)

        return context

    def get_extra_urls(self) -> list[URLPattern]:
        self.extra_button_handlers.clear()
        handlers: dict[str, BaseExtraHandler] = {}
        extra_urls: list[URLPattern] = []
        opts = self.model._meta
        for cls in inspect.getmro(self.__class__):
            for method_name, method in cls.__dict__.items():
                if callable(method) and isinstance(method, BaseExtraHandler):
                    handlers[method_name] = method.get_instance(self)

        handler: BaseExtraHandler
        for handler in handlers.values():
            handler.url_name = f"{opts.app_label}_{opts.model_name}_{handler.func.__name__}"
            if isinstance(handler, ViewHandler) and handler.url_pattern:
                f = partial(getattr(self, handler.func.__name__), self)
                for deco in handler.decorators[::-1]:
                    f = deco(f)
                extra_urls.append(path(handler.url_pattern, f, name=handler.url_name))
            if isinstance(handler, (ButtonHandler, LinkHandler, ChoiceHandler)):
                self.extra_button_handlers[handler.func.__name__] = handler
        return extra_urls

    def get_urls(self) -> list[URLPattern]:
        urls = self.get_extra_urls()
        urls.extend(super().get_urls())
        return urls

    def get_changeform_buttons(self, context: RequestContext) -> list[HandlerWithButton]:  # noqa: ARG002,
        return [h for h in self.extra_button_handlers.values() if h.change_form in {True, None}]

    def get_changelist_buttons(self, context: RequestContext) -> list[HandlerWithButton]:  # noqa: ARG002,
        return [h for h in self.extra_button_handlers.values() if h.change_list in {True, None}]

    def get_action_buttons(self, context: RequestContext) -> list[HandlerWithButton]:  # noqa: ARG002, PLR6301
        return []

    @property
    def media(self) -> forms.Media:
        extra = "" if settings.DEBUG else ".min"
        base = super().media
        return base + forms.Media(
            js=[
                f"admin/js/vendor/jquery/jquery{extra}.js",
                "admin/js/jquery.init.js",
                f"admin_extra_buttons{extra}.js",
            ],
            css={
                "screen": ("admin_extra_buttons.css",),
            },
        )
