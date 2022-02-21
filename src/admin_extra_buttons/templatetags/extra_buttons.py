from django import template

register = template.Library()


@register.filter
def default_if_empty(v, default):
    if v and v.strip():
        return v
    return default


@register.simple_tag(takes_context=True)
def get_action_buttons(context, model_admin):
    return [handler.get_button(context)
            for handler in model_admin.get_action_buttons(context)]


@register.simple_tag(takes_context=True)
def get_changeform_buttons(context, model_admin):
    return [handler.get_button(context)
            for handler in model_admin.get_changeform_buttons(context)]


@register.simple_tag(takes_context=True)
def get_changelist_buttons(context, model_admin):
    return [handler.get_button(context)
            for handler in model_admin.get_changelist_buttons(context)]
