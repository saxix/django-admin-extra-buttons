import inspect

from django.http import HttpResponse
from django.utils.functional import cached_property

from .buttons import LinkButton, ViewButton
from .utils import HttpResponseRedirectToReferrer, check_permission, labelize


class BaseExtraHandler:
    """Decorator example mixing class and function definitions."""

    def __init__(self, func, **kwargs):
        self.func = func
        self.options = kwargs
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

        ret = self.func(model_admin, request, *args, **kwargs)

        if not isinstance(ret, HttpResponse):
            return HttpResponseRedirectToReferrer(request)
        return ret


class ViewHandler(BaseExtraHandler):
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
