from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.core.exceptions import PermissionDenied
from django.template.loader import get_template
from django.urls import NoReverseMatch, reverse

from admin_extra_buttons.utils import check_permission, get_preserved_filters, labelize

if TYPE_CHECKING:
    from collections.abc import Callable, Generator

    from django.contrib.admin import AdminSite
    from django.db.models import Model
    from django.http import HttpRequest
    from django.template import RequestContext
    from django.template.backends.base import _EngineTemplate

    from admin_extra_buttons.handlers import BaseExtraHandler


class ButtonWidget:
    default_change_form_arguments = 2
    default_template = "admin_extra_buttons/includes/button.html"

    def __init__(  # noqa: PLR0913, PLR0917
        self,
        handler: "BaseExtraHandler",
        context: "RequestContext",
        label: str | None = None,
        visible: "bool|Callable[[ButtonWidget], bool]" = True,
        enabled: "bool|Callable[[ButtonWidget], bool]" = True,
        change_form: bool | None = None,
        change_list: bool | None = None,
        template: str | None = None,
        **config: Any,
    ) -> None:
        self.label = label
        self.url_pattern = config.get("url_pattern")
        self.href = config.get("href") or ""
        self.config = config
        self.handler: BaseExtraHandler = handler
        self._visible = visible
        self._enabled = enabled
        self.template = template or self.default_template
        self.context: "RequestContext" = context
        self.disable_on_click = True
        self.disable_on_edit = True
        self.change_form = self.get_change_form_flag(change_form)
        self.change_list = self.get_change_list_flag(change_list)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} '{self.label}'>"

    def __str__(self) -> str:
        tpl: _EngineTemplate = get_template(self.template)
        return tpl.render(self.context.flatten())  # type:ignore[arg-type]

    def get_change_form_flag(self, arg: Any | None) -> bool:
        if arg is None:  # pragma: no branch
            return len(self.handler.func_args) > self.default_change_form_arguments
        return bool(arg)

    def get_change_list_flag(self, arg: Any | None) -> bool:
        if arg is None:  # pragma: no branch
            return len(self.handler.func_args) == self.default_change_form_arguments
        return bool(arg)

    @property
    def html_attrs(self) -> dict[str, str]:
        attrs = self.config.get("html_attrs", {}) or {}
        if "id" not in attrs:
            attrs["id"] = f"btn-{self.handler.func.__name__}"

        css_class = attrs.get("class", "")
        css_class += " aeb-button"
        if self.disable_on_click and "aeb-disable-on-click" not in css_class:
            css_class += " aeb-disable-on-click"
        if self.disable_on_edit and "aeb-disable_on_edit" not in css_class:
            css_class += " aeb-disable_on_edit"

        css_class = css_class.replace("disabled", "")
        if self.enabled:
            css_class += " enabled"
        else:
            css_class += " disabled"

        attrs["class"] = css_class
        return attrs

    def can_render(self) -> bool:
        return self.authorized() and bool(self.url) and self.visible

    @property
    def enabled(self) -> bool:
        if not self.context:  # pragma: no cover
            raise ValueError("Button not initialised.")
        if callable(self._enabled):
            return self._enabled(self)

        return self._enabled

    @property
    def admin_site(self) -> AdminSite:
        return self.handler.model_admin.admin_site

    @property
    def visible(self) -> bool:
        if not self.context:  # pragma: no cover
            raise ValueError("Button not initialised.")
        if callable(self._visible):
            return self._visible(self)
        return self._visible

    @visible.setter
    def visible(self, value: bool) -> None:
        self._visible = value

    @property
    def request(self) -> "HttpRequest":
        if not self.context:  # pragma: no cover
            raise ValueError("Button not initialised.")
        return self.context["request"]  # type:ignore[no-any-return]

    @property
    def original(self) -> Model | None:
        if not self.context:  # pragma: no cover
            raise ValueError("Button not initialised.")
        return self.context.get("original", None)

    def authorized(self) -> bool:
        if self.handler.permission:
            try:
                return check_permission(self.handler, self.handler.permission, self.request, self.original)
            except PermissionDenied:
                return False
        return True

    @property
    def url(self) -> str:
        if not self.enabled:
            return "#"
        func: "Callable[[RequestContext], str]" = self.config.get("get_url", self.get_url)
        return func(self.context)

    def get_url(self, context: "RequestContext") -> str | None:  # noqa: ARG002
        detail = len(self.handler.func_args) > self.default_change_form_arguments
        try:
            if self.change_form and self.original and detail:
                url_ = reverse(f"{self.admin_site.name}:{self.handler.url_name}", args=[self.original.pk])
            elif self.change_list:
                url_ = reverse(f"{self.admin_site.name}:{self.handler.url_name}")
            else:
                return None
        except NoReverseMatch:  # pragma: no cover
            return None
        filters = get_preserved_filters(self.request)
        return f"{url_}?{filters}"


class LinkButton(ButtonWidget):
    @property
    def url(self) -> str:
        return self.href

    def get_change_form_flag(self, arg: Any | None) -> bool:  # noqa: PLR6301
        if arg is None:
            return True
        return bool(arg)

    def get_change_list_flag(self, arg: Any | None) -> bool:  # noqa: PLR6301
        if arg is None:
            return True
        return bool(arg)


class ChoiceButton(LinkButton):
    default_template = "admin_extra_buttons/includes/choice.html"

    def __init__(  # noqa: PLR0917, PLR0913
        self,
        handler: "BaseExtraHandler",
        context: "RequestContext",
        label: str | None = None,
        visible: bool = True,
        enabled: bool = True,
        change_form: bool | None = None,
        change_list: bool | None = None,
        template: str | None = None,
        **config: Any,
    ) -> None:
        self.choices: list[BaseExtraHandler] = []
        super().__init__(handler, context, label, visible, enabled, change_form, change_list, template, **config)

    def get_choices(self) -> Generator[dict[str, Any], None, None]:
        for handler_config in self.choices:
            handler = handler_config.func.extra_buttons_handler
            if self.change_list and handler.single_object_invocation:
                url = reverse(f"admin:{handler.url_name}")
            elif not handler.single_object_invocation and self.change_form and self.original:
                url = reverse(f"admin:{handler.url_name}", args=[self.context["original"].pk])
            else:
                url = None
            if url:
                yield {
                    "label": handler.config.get("label", labelize(handler.name)),
                    "url": url,
                    "selected": self.request.path == url,
                }

    def can_render(self) -> bool:  # noqa: PLR6301
        return True

    @property
    def html_attrs(self) -> dict[str, str]:
        ret = super().html_attrs
        ret.setdefault("name", self.handler.name)
        return ret
