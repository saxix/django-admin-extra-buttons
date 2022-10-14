import inspect
import logging
from functools import partial

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.db import OperationalError, ProgrammingError
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse

from .handlers import BaseExtraHandler, ViewHandler

logger = logging.getLogger(__name__)

IS_GRAPPELLI_INSTALLED = 'grappelli' in settings.INSTALLED_APPS

NOTSET = object()


class ActionFailed(Exception):
    pass


def confirm_action(modeladmin, request,
                   action, message,
                   success_message='',
                   description='',
                   pk=None,
                   extra_context=None,
                   title=None,
                   template='admin_extra_buttons/confirm.html',
                   error_message=None):
    opts = modeladmin.model._meta
    if extra_context:
        title = extra_context.pop('title', title)
    context = modeladmin.get_common_context(request,
                                            message=message,
                                            description=description,
                                            title=title,
                                            pk=pk,
                                            **(extra_context or {}))
    if request.method == 'POST':
        ret = None
        try:
            ret = action(request)
            modeladmin.message_user(request, success_message, messages.SUCCESS)
        except Exception as e:  # pragma: no cover
            modeladmin.message_user(request, error_message or str(e), messages.ERROR)

        return ret or HttpResponseRedirect(reverse(admin_urlname(opts, 'changelist')))

    return TemplateResponse(request, template, context)


class ExtraUrlConfigException(RuntimeError):
    pass


class DummyAdminform:
    def __init__(self, **kwargs):
        self.prepopulated_fields = []
        self.__dict__.update(**kwargs)

    def __iter__(self):  # pragma: no cover
        yield


class ExtraButtonsMixin:
    _registered_buttons = []
    if IS_GRAPPELLI_INSTALLED:  # pragma: no cover
        change_list_template = 'admin_extra_buttons/grappelli/change_list.html'
        change_form_template = 'admin_extra_buttons/grappelli/change_form.html'
    else:
        change_list_template = 'admin_extra_buttons/change_list.html'
        change_form_template = 'admin_extra_buttons/change_form.html'

    def __init__(self, model, admin_site):
        self.extra_button_handlers = {}
        super().__init__(model, admin_site)

    def message_error_to_user(self, request, exception):
        self.message_user(request, f'{exception.__class__.__name__}: {exception}', messages.ERROR)

    @classmethod
    def check(cls, **kwargs):
        errors = []
        try:
            from admin_extra_buttons.utils import check_decorator_errors
            errors.extend(check_decorator_errors(cls))
        except (OSError, OperationalError, ProgrammingError):  # pragma: no cover
            pass
        return errors

    def get_common_context(self, request, pk=None, **kwargs):
        opts = self.model._meta
        app_label = opts.app_label
        self.object = None

        context = {
            **self.admin_site.each_context(request),
            **kwargs,
            'opts': opts,
            'add': False,
            'change': True,
            'save_as': False,
            'extra_buttons': self.extra_button_handlers,
            'has_delete_permission': self.has_delete_permission(request, pk),
            'has_editable_inline_admin_formsets': False,
            'has_view_permission': self.has_view_permission(request, pk),
            'has_change_permission': self.has_change_permission(request, pk),
            'has_add_permission': self.has_add_permission(request),
            'app_label': app_label,
            'adminform': DummyAdminform(model_admin=self),
        }
        context.setdefault('title', '')
        context.update(**kwargs)
        if pk:
            self.object = self.get_object(request, pk)
            context['original'] = self.object
        return context

    def get_extra_urls(self) -> list:
        self.extra_button_handlers = {}
        handlers = {}
        extra_urls = []
        opts = self.model._meta
        for cls in inspect.getmro(self.__class__):
            for method_name, method in cls.__dict__.items():
                if callable(method) and isinstance(method, BaseExtraHandler):
                    handlers[method_name] = method.get_instance(self)

        handler: ViewHandler
        for handler in handlers.values():
            handler.url_name = f'{opts.app_label}_{opts.model_name}_{handler.func.__name__}'
            if handler.url_pattern:
                f = partial(getattr(self, handler.func.__name__), self)
                for deco in handler.decorators[::-1]:
                    f = deco(f)
                extra_urls.append(path(handler.url_pattern,
                                       f,
                                       name=handler.url_name))
            if hasattr(handler, 'button_class'):
                self.extra_button_handlers[handler.func.__name__] = handler
        return extra_urls

    def get_urls(self):
        urls = self.get_extra_urls()
        urls.extend(super().get_urls())
        return urls

    def get_changeform_buttons(self, context):
        return [h for h in self.extra_button_handlers.values() if h.change_form in [True, None]]

    def get_changelist_buttons(self, context):
        return [h for h in self.extra_button_handlers.values() if h.change_list in [True, None]]

    def get_action_buttons(self, context):
        return []

    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'
        base = super().media
        return base + forms.Media(
            js=[
                'admin/js/vendor/jquery/jquery%s.js' % extra,
                'admin/js/jquery.init.js',
                'admin_extra_buttons%s.js' % extra,
            ],
            css={
                'screen': (
                    'admin_extra_buttons.css',
                ),
            },
        )
