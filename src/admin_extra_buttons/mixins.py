"""
Django admin extra buttons mixins.

Usage:
    from admin_extra_buttons.mixins import ExtraButtonsMixin
    from admin_extra_buttons.decorators import button

    @admin.register(MyModel)
    class MyModelAdmin(ExtraButtonsMixin, admin.ModelAdmin):
        @button(html_attrs={"title": "My Button"}, change_list=True)
        def my_button(self, request):
            # Your button logic here
            ...
"""
import inspect
from typing import TYPE_CHECKING, Any

from django.contrib import admin
from django.db.models import Model
from django.urls import URLPattern, path

from .handlers import ButtonHandler

if TYPE_CHECKING:
    from django.contrib.admin import AdminSite


class BaseButtonsMixin:
    """
    Base mixin providing the core logic for discovering buttons and creating URLs.
    This class is not meant to be used directly.
    """

    def __init__(self, model: type[Model], admin_site: "AdminSite") -> None:
        self.extra_button_handlers: dict[str, ButtonHandler] = {}
        super().__init__(model, admin_site)

    def get_extra_urls(self) -> list[URLPattern]:
        """Discover ButtonHandler methods and create corresponding URL patterns."""
        self.extra_button_handlers.clear()
        handlers: dict[str, ButtonHandler] = {}
        opts = self.model._meta

        # Introspect the MRO to find all ButtonHandler instances
        for cls in inspect.getmro(self.__class__):
            for method_name, method in cls.__dict__.items():
                if isinstance(method, ButtonHandler):
                    handler = method.get_instance(self)
                    handler.method_name = method_name
                    handlers[method_name] = handler

        extra_urls: list[URLPattern] = []
        for method_name, handler in handlers.items():
            handler.url_name = f"{opts.app_label}_{opts.model_name}_{method_name}"
            self.extra_button_handlers[method_name] = handler

            # The view is the handler instance itself, which is callable
            view = self.admin_site.admin_view(handler)
            url_pattern = f"{method_name}/"
            extra_urls.append(path(url_pattern, view, name=handler.url_name))
        return extra_urls

    def get_urls(self) -> list[URLPattern]:
        """Append the extra button URLs to the admin URLs."""
        return self.get_extra_urls() + super().get_urls()

    def get_changelist_buttons(self) -> list[ButtonHandler]:
        """Get buttons to be displayed on the changelist page."""
        return [
            handler
            for handler in self.extra_button_handlers.values()
            if handler.change_list is not False  # Show if True or None
        ]

    def get_changeform_buttons(self) -> list[ButtonHandler]:
        """Get buttons to be displayed on the change form page."""
        return [
            handler
            for handler in self.extra_button_handlers.values()
            if handler.change_form is not False  # Show if True or None
        ]


class LightweightButtonsMixin(BaseButtonsMixin):
    """
    Adds buttons to the admin by passing them to the template context.

    This mixin requires you to extend the admin templates to include
    the rendering logic for the buttons.
    """

    def changelist_view(self, request: Any, extra_context: dict | None = None) -> Any:
        """Add changelist buttons to the template context."""
        extra_context = extra_context or {}
        extra_context["custom_buttons"] = self.get_changelist_buttons()
        return super().changelist_view(request, extra_context)

    def change_view(
        self,
        request: Any,
        object_id: Any,
        form_url: str = "",
        extra_context: dict | None = None,
    ) -> Any:
        """Add change form buttons to the template context."""
        extra_context = extra_context or {}
        extra_context["custom_buttons"] = self.get_changeform_buttons()
        return super().change_view(request, object_id, form_url, extra_context)


class ExtraButtonsMixin(LightweightButtonsMixin):
    """
    A "batteries-included" mixin that automatically adds buttons.

    This mixin overrides the admin templates to provide a zero-configuration
    setup. It inherits all logic from LightweightButtonsMixin and simply
    points to its own templates.
    """

    change_list_template = "admin_extra_buttons/change_list.html"
    change_form_template = "admin_extra_buttons/change_form.html"


__all__ = [
    "ExtraButtonsMixin",
    "LightweightButtonsMixin",
    "BaseButtonsMixin",
]
