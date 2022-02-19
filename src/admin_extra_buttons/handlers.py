import inspect

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.utils.functional import cached_property

from .buttons import LinkButton, ViewButton
from .utils import HttpResponseRedirectToReferrer, check_permission, labelize, handle_basic_auth


class BaseExtraHandler:
    """Decorator example mixing class and function definitions."""

    def __init__(self, func, **kwargs):
        self.func = func
        self.options = kwargs
        self.login_required = kwargs.get('login_required', True)
        self.pattern = kwargs.get('pattern', None)
        self.permission = kwargs.get('permission')
        self.sig: inspect.Signature = inspect.signature(self.func)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name}>"

    def get_instance(self):
        return self.__class__(self.func, **self.options)

    @cached_property
    def name(self):
        return self.func.__name__

    def __call__(self, model_admin, request, *args, **kwargs):
        obj = None
        if len(self.sig.parameters) > 2:
            pk = kwargs.get(list(self.sig.parameters)[2])
            obj = model_admin.get_object(request, pk)

        if self.permission:
            check_permission(self.permission, request, obj)
        elif self.login_required and not request.user.is_authenticated:
            raise PermissionDenied

        ret = self.func(model_admin, request, *args, **kwargs)

        if not isinstance(ret, HttpResponse):
            return HttpResponseRedirectToReferrer(request)
        return ret


class ViewHandler(BaseExtraHandler):
    def __init__(self, func, login_required=True, http_basic_auth=False, **kwargs):
        self.login_required = login_required
        self.http_basic_auth = http_basic_auth
        super().__init__(func,
                         http_basic_auth=http_basic_auth,
                         login_required=login_required,
                         **kwargs)

    def __call__(self, model_admin, request, *args, **kwargs):
        if self.login_required and self.http_basic_auth and not request.user.is_authenticated:
            handle_basic_auth(request)
        return super().__call__(model_admin, request, *args, **kwargs)

    @cached_property
    def url_pattern(self):
        if self.pattern:
            return self.pattern
        else:
            pattern = ''
            for arg in list(self.sig.parameters)[2:]:
                pattern += f'<path:{arg}>/'
            pattern += f'{self.name}/'
        return pattern


class ButtonMixin:

    def __init__(self, func, html_attrs=None, change_list=None, change_form=None, **kwargs):
        self.change_form = change_form
        self.change_list = change_list
        self.html_attrs = html_attrs or {}
        super().__init__(func, change_form=change_form,
                         change_list=change_list,
                         html_attrs=html_attrs,
                         **kwargs)

    def get_button_params(self, context, **extra):
        return {'label': self.options.get('label', labelize(self.name)),
                'handler': self,
                'html_attrs': self.html_attrs,
                'change_list': self.change_list,
                'change_form': self.change_form,
                'context': context,
                'login_required': self.login_required,
                'permission': self.permission,
                **extra
                }

    def get_button(self, context):
        return self.button_class(**self.get_button_params(context))


class ButtonHandler(ButtonMixin, ViewHandler):
    button_class = ViewButton


class LinkHandler(ButtonMixin, BaseExtraHandler):
    button_class = LinkButton
    url_pattern = None

    def __init__(self, func, href, **kwargs):
        self.href = href
        super().__init__(func, href=href, **kwargs)

    def get_button_params(self, context, **extra):
        return super().get_button_params(context,
                                         href=self.href,
                                         url_pattern=self.url_pattern,
                                         )

    def get_button(self, context):
        params = self.get_button_params(context)
        button = self.button_class(**params)
        self.func(self, button)
        return button
