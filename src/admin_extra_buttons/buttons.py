from django.core.exceptions import PermissionDenied
from django.urls import NoReverseMatch, reverse

from admin_extra_buttons.utils import check_permission, get_preserved_filters


class ViewButton:
    def __init__(self, handler, context, label=None,
                 change_form=None, change_list=None, **options):
        self.label = label
        self.url_pattern = options.get('url_pattern', None)
        self.href = options.get('href', None)
        self.options = options
        self.handler = handler
        self.context = context

        self.change_form = self.get_change_form_flag(change_form)
        self.change_list = self.get_change_list_flag(change_list)

    def __repr__(self):
        return f"<ViewButton '{self.label}' {self.handler}>"

    def get_change_form_flag(self, arg):
        if arg is None:  # pragma: no cover
            return len(self.handler.sig.parameters) > 2
        return arg

    def get_change_list_flag(self, arg):
        if arg is None:  # pragma: no cover
            return len(self.handler.sig.parameters) == 2
        return arg

    @property
    def html_attrs(self):
        attrs = self.options.get('html_attrs', {})
        if 'id' not in attrs:
            attrs['id'] = f'btn-{self.handler.func.__name__}'
        return attrs

    @property
    def request(self):
        if not self.context:
            raise ValueError(f"You need to call bind() to access 'request' on {self}")
        return self.context['request']

    @property
    def original(self):
        if not self.context:
            raise ValueError(f"You need to call bind() to access 'original' on {self}")
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
