from typing import TYPE_CHECKING

from django import template

from admin_extra_buttons.mixins import ExtraButtonsMixin

if TYPE_CHECKING:
    from django.template import RequestContext

    from admin_extra_buttons.types import VisibleButton


register = template.Library()


@register.filter
def default_if_empty(v: str, default: str) -> str:
    if v and v.strip():
        return v
    return default


@register.simple_tag(takes_context=True)
def get_action_buttons(context: "RequestContext", model_admin: ExtraButtonsMixin) -> "list[VisibleButton]":
    return [handler.get_button(context) for handler in model_admin.get_action_buttons(context)]


@register.simple_tag(takes_context=True)
def get_changeform_buttons(context: "RequestContext", model_admin: ExtraButtonsMixin) -> "list[VisibleButton]":
    return [handler.get_button(context) for handler in model_admin.get_changeform_buttons(context)]


@register.simple_tag(takes_context=True)
def get_changelist_buttons(context: "RequestContext", model_admin: ExtraButtonsMixin) -> "list[VisibleButton]":
    return [handler.get_button(context) for handler in model_admin.get_changelist_buttons(context)]
