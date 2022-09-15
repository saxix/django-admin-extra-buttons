import inspect

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.utils.functional import cached_property

from .buttons import Button, ChoiceButton, LinkButton
from .utils import HttpResponseRedirectToReferrer, check_permission, handle_basic_auth, labelize


class BaseExtraHandler:
    def __init__(self, func, **kwargs):
        self.func = func
        self.func._handler = self
        self.config = kwargs
        self.model_admin = kwargs.get('model_admin', None)
        self.decorators = kwargs.get('decorators', [])
        self.login_required = kwargs.get('login_required', True)
        self._pattern = kwargs.get('pattern', None)
        self.permission = kwargs.get('permission')
        self.sig: inspect.Signature = inspect.signature(self.func)

    @cached_property
    def func_args(self):
        return list(self.sig.parameters)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name}>"

    def get_instance(self, model_admin):
        """ return a 'clone' of current Handler"""
        return self.__class__(self.func, model_admin=model_admin, **self.config)

    @cached_property
    def name(self):
        return self.func.__name__

    def __call__(self, model_admin, request, *args, **kwargs):
        obj = None
        self.model_admin = model_admin
        if len(self.sig.parameters) > 2:
            pk = kwargs.get(list(self.sig.parameters)[2])
            obj = model_admin.get_object(request, pk)

        if self.permission:
            check_permission(self, self.permission, request, obj)
        elif self.login_required and not request.user.is_authenticated:
            raise PermissionDenied

        ret = self.func(model_admin, request, *args, **kwargs)

        if not isinstance(ret, HttpResponse):
            return HttpResponseRedirectToReferrer(request)
        return ret


class ViewHandler(BaseExtraHandler):
    def __init__(self, func, login_required=True, http_basic_auth=False, http_auth_handler=None, **kwargs):
        self.login_required = login_required
        if http_auth_handler:
            if http_basic_auth:
                raise ValueError("'http_basic_auth' and 'http_auth_handler' are mutually exclusive")
            self.http_auth_handler = http_auth_handler
        else:
            self.http_basic_auth = http_basic_auth
            self.http_auth_handler = handle_basic_auth
        super().__init__(func,
                         http_auth_handler=http_auth_handler,
                         http_basic_auth=http_basic_auth,
                         login_required=login_required,
                         **kwargs)

    def __call__(self, model_admin, request, *args, **kwargs):
        self.model_admin = model_admin
        if self.login_required and self.http_basic_auth and not request.user.is_authenticated:
            self.http_auth_handler(request)
        return super().__call__(model_admin, request, *args, **kwargs)

    @cached_property
    def url_pattern(self):
        if self._pattern:
            return self._pattern
        else:
            pattern = ''
            for arg in list(self.sig.parameters)[2:]:
                pattern += f'<path:{arg}>/'
            pattern += f'{self.name}/'
        return pattern


class ButtonMixin:

    def __init__(self, func, html_attrs=None,
                 change_list=None, change_form=None, visible=True, enabled=True, **kwargs):
        self.change_form = change_form
        self.change_list = change_list
        self.visible = visible
        self.enabled = enabled
        self.html_attrs = html_attrs or {}
        super().__init__(func, change_form=change_form,
                         change_list=change_list,
                         html_attrs=html_attrs,
                         enabled=enabled,
                         visible=visible,
                         **kwargs)

    def get_button_params(self, context, **extra):
        return {'label': self.config.get('label', labelize(self.name)),
                'handler': self,
                'html_attrs': self.html_attrs,
                'change_list': self.change_list,
                'change_form': self.change_form,
                'visible': self.visible,
                'enabled': self.enabled,
                'context': context,
                'login_required': self.login_required,
                'permission': self.permission,
                **extra
                }

    def get_button(self, context):
        return self.button_class(**self.get_button_params(context))


class ButtonHandler(ButtonMixin, ViewHandler):
    """View handler for `@button` decorated views"""
    button_class = Button


class LinkHandler(ButtonMixin, BaseExtraHandler):
    button_class = LinkButton
    url_pattern = None

    def __init__(self, func, **kwargs):
        self.href = kwargs.pop('href', None)
        super().__init__(func, href=self.href, **kwargs)

    def get_button_params(self, context, **extra):
        return super().get_button_params(context,
                                         href=self.href,
                                         url_pattern=self.url_pattern,
                                         **extra,
                                         )

    def get_button(self, context):
        params = self.get_button_params(context)
        button = self.button_class(**params)
        self.func(self.model_admin, button)
        return button


class ChoiceHandler(LinkHandler):
    button_class = ChoiceButton

    def __init__(self, func, **kwargs):
        self.href = kwargs.pop('href', None)
        self.choices = kwargs.pop('choices', None)
        self.selected_choice = None
        super().__init__(func, href=self.href, choices=self.choices, **kwargs)

    def get_button_params(self, context, **extra):
        return super().get_button_params(context,
                                         choices=self.choices,
                                         **extra,
                                         )
