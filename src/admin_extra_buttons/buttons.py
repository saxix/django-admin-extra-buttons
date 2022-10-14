from django.core.exceptions import PermissionDenied
from django.template import RequestContext, Template
from django.template.loader import get_template
from django.urls import NoReverseMatch, reverse

from admin_extra_buttons.utils import check_permission, get_preserved_filters, labelize


class Button:
    default_change_form_arguments = 2
    default_template = "admin_extra_buttons/includes/button.html"

    def __init__(self, handler, context, label=None, visible=True, enabled=True,
                 change_form=None, change_list=None, template=None, **config):
        self.label = label
        self.url_pattern = config.get('url_pattern', None)
        self.href = config.get('href', None)
        self.config = config
        self.handler = handler
        self._visible = visible
        self._enabled = enabled
        self.template = template or self.default_template
        self.context: RequestContext = context
        self.disable_on_click = True
        self.disable_on_edit = True
        self.change_form = self.get_change_form_flag(change_form)
        self.change_list = self.get_change_list_flag(change_list)

    def __repr__(self):
        return f"<{self.__class__.__name__} '{self.label}'>"

    def __str__(self):
        tpl: Template = get_template(self.template)
        return tpl.render(self.context.flatten())

    def get_change_form_flag(self, arg):
        if arg is None:  # pragma: no branch
            return len(self.handler.func_args) > self.default_change_form_arguments
        return arg

    def get_change_list_flag(self, arg):
        if arg is None:  # pragma: no branch
            return len(self.handler.func_args) == self.default_change_form_arguments
        return arg

    @property
    def html_attrs(self):
        attrs = self.config.get('html_attrs', {})
        if 'id' not in attrs:
            attrs['id'] = f'btn-{self.handler.func.__name__}'

        css_class = attrs.get("class", "")

        if self.disable_on_click and "aeb-disable-on-click" not in css_class:
            css_class += " aeb-disable-on-click"
        if self.disable_on_edit and "aeb-disable_on_edit" not in css_class:
            css_class += " aeb-disable_on_edit"

        css_class = css_class.replace("disabled", "")
        if self.enabled:
            css_class += " enabled"
        else:
            css_class += " disabled"

        attrs['class'] = css_class
        return attrs

    def can_render(self):
        return self.authorized() and self.url and self.visible

    @property
    def enabled(self):
        if not self.context:  # pragma: no cover
            raise ValueError("Button not initialised.")
        if callable(self._enabled):
            try:
                return self._enabled(self)
            except Exception:  # pragma: no cover
                return False

        return self._enabled

    @property
    def model_admin(self):
        return self.handler.model_admin

    @property
    def admin_site(self):
        return self.handler.model_admin.admin_site

    @property
    def visible(self):
        if not self.context:  # pragma: no cover
            raise ValueError("Button not initialised.")
        if callable(self._visible):
            try:
                return self._visible(self)
            except Exception:  # pragma: no cover
                return False

        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value

    @property
    def request(self):
        if not self.context:  # pragma: no cover
            raise ValueError("Button not initialised.")
        return self.context['request']

    @property
    def original(self):
        if not self.context:  # pragma: no cover
            raise ValueError("Button not initialised.")
        return self.context.get('original', None)

    def authorized(self):
        if self.handler.permission:
            try:
                return check_permission(self.handler,
                                        self.handler.permission, self.request, self.original)
            except PermissionDenied:
                return False
        return True

    @property
    def url(self):
        if not self.enabled:
            return '#'
        func = self.config.get('get_url', self.get_url)
        return func(self.context)

    def get_url(self, context):
        detail = len(self.handler.sig.parameters) > self.default_change_form_arguments
        try:
            if self.change_form and self.original and detail:
                url_ = reverse(f'{self.admin_site.name}:{self.handler.url_name}', args=[self.original.pk])
            elif self.change_list:
                url_ = reverse(f'{self.admin_site.name}:{self.handler.url_name}')
            else:
                return None
            filters = get_preserved_filters(self.request)
            return f'{url_}?{filters}'
        except NoReverseMatch:  # pragma: no cover
            return None


class LinkButton(Button):
    @property
    def url(self):
        return self.href

    def get_change_form_flag(self, arg):
        if arg is None:
            return True
        return arg

    def get_change_list_flag(self, arg):
        if arg is None:
            return True
        return arg


class ChoiceButton(LinkButton):
    default_template = "admin_extra_buttons/includes/choice.html"

    def get_choices(self):
        for handler_config in self.choices:
            handler = handler_config.func._handler
            if self.change_list and len(handler.func_args) == 2:
                url = reverse(f"admin:{handler.url_name}")
            elif len(handler.func_args) > 2 and self.change_form and self.original:
                url = reverse(f"admin:{handler.url_name}", args=[self.context['original'].pk])
            else:
                url = None
            if url:
                yield {"label": handler.config.get('label', labelize(handler.name)),
                       "url": url,
                       "selected": self.request.path == url,
                       }
        return []

    def can_render(self):
        return True

    @property
    def html_attrs(self):
        ret = super().html_attrs
        ret.setdefault('name', self.handler.name)
        return ret
