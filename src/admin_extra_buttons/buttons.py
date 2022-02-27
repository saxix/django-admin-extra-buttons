from django.core.exceptions import PermissionDenied
from django.urls import NoReverseMatch, reverse

from admin_extra_buttons.utils import check_permission, get_preserved_filters


class ViewButton:
    def __init__(self, handler, context, label=None, visible=True, enabled=True,
                 change_form=None, change_list=None, **options):
        self.label = label
        self.url_pattern = options.get('url_pattern', None)
        self.href = options.get('href', None)
        self.options = options
        self.handler = handler
        self.visible = visible
        self.enabled = enabled
        self.context = context
        self.disable_on_click = True
        self.disable_on_edit = True
        self.change_form = self.get_change_form_flag(change_form)
        self.change_list = self.get_change_list_flag(change_list)

    def __repr__(self):
        return f"<ViewButton '{self.label}' {self.handler.name}>"

    def get_change_form_flag(self, arg):
        if arg is None:  # pragma: no cover
            return len(self.handler.func_args) > 2
        return arg

    def get_change_list_flag(self, arg):
        if arg is None:  # pragma: no branch
            return len(self.handler.func_args) == 2
        return arg

    @property
    def html_attrs(self):
        attrs = self.options.get('html_attrs', {})
        if 'id' not in attrs:
            attrs['id'] = f'btn-{self.handler.func.__name__}'

        css_class = attrs.get("class", "")

        if self.disable_on_click and "aeb-disable-on-click" not in css_class:
            css_class += " aeb-disable-on-click"
        if self.disable_on_edit and "aeb-disable_on_edit" not in css_class:
            css_class += " aeb-disable_on_edit"

        # enabled
        css_class= css_class.replace("disabled", "")
        if not self.enabled:
            css_class += " disabled"
        elif callable(self.enabled) and not self.enabled(self):
            css_class += " disabled"

        attrs['class'] = css_class
        return attrs

    def can_render(self):
        return self.authorized() and self.url and self.is_visible()

    def is_visible(self):
        if not self.context:  # pragma: no cover
            raise ValueError("Button not initialised.")
        if callable(self.visible):
            try:
                return self.visible(self)
            except Exception:  # pragma: no cover
                return False

        return self.visible

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
                return check_permission(self.handler.permission, self.request, self.original)
            except PermissionDenied:
                return False
        return True

    @property
    def url(self):
        func = self.options.get('get_url', self.get_url)
        return func(self.context)

    def get_url(self, context):
        detail = len(self.handler.sig.parameters) > 2
        try:
            if self.change_form and self.original and detail:
                url_ = reverse(f'admin:{self.handler.url_name}', args=[self.original.pk])
            elif self.change_list:
                url_ = reverse(f'admin:{self.handler.url_name}')
            else:
                return None
            filters = get_preserved_filters(self.request)
            return f'{url_}?{filters}'
        except NoReverseMatch:  # pragma: no cover
            return None


class LinkButton(ViewButton):
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
