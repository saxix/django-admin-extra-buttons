django-admin-extra-buttons
==========================


[![Pypi](https://badge.fury.io/py/django-admin-extra-buttons.svg)](https://badge.fury.io/py/django-admin-extra-buttons)
[![coverage](https://codecov.io/github/saxix/django-admin-extra-buttons/coverage.svg?branch=develop)](https://codecov.io/github/saxix/django-admin-extra-buttons?branch=develop)
[![Test](https://github.com/saxix/django-admin-extra-buttons/actions/workflows/test.yml/badge.svg)](https://github.com/saxix/django-admin-extra-buttons/actions/workflows/test.yml)
[![Docs](https://github.com/saxix/django-admin-extra-buttons/actions/workflows/docs.yml/badge.svg)](https://github.com/saxix/django-admin-extra-buttons/actions/workflows/docs.yml)

![my image](https://raw.githubusercontent.com/saxix/django-admin-extra-buttons/develop/docs/images/screenshot.png)

This is a full rewriting of the original `django-admin-extra-url`. It
provides decorators to easily add custom buttons to Django Admin pages and/or add views to any ModelAdmin

It allows easy creation of wizards, actions and/or links to external resources 
as well as api only views.

Three decorators are available: 

- ``button()`` to mark a method as extra view and show related button
- ``link()`` This is used for "external" link, where you don't need to invoke local views.
- ``view()`` View only decorator, this adds a new url but do not render any button.


Install
-------

    pip install django-admin-extra-buttons


After installation add it to ``INSTALLED_APPS``

    INSTALLED_APPS = (
       ...
       'admin_extra_buttons',
    )

How to use it
-------------

```python

from admin_extra_buttons.api import ExtraButtonsMixin, button, confirm_action, link, view
from admin_extra_buttons.utils import HttpResponseRedirectToReferrer
from django.http import HttpResponse, JsonResponse
from django.contrib import admin
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.csrf import csrf_exempt

class MyModelModelAdmin(ExtraButtonsMixin, admin.ModelAdmin):

    @button(permission='demo.add_demomodel1',
            change_form=True,
            html_attrs={'style': 'background-color:#88FF88;color:black'})
    def refresh(self, request):
        self.message_user(request, 'refresh called')
        # Optional: returns HttpResponse
        return HttpResponseRedirectToReferrer(request)
    
    @button(html_attrs={'style': 'background-color:#DC6C6C;color:black'})
    def confirm(self, request):
        def _action(request):
            pass

        return confirm_action(self, request, _action, "Confirm action",
                          "Successfully executed", )

    @link(href=None, 
          change_list=False, 
          html_attrs={'target': '_new', 'style': 'background-color:var(--button-bg)'})
    def search_on_google(self, button):
        original = button.context['original']
        button.label = f"Search '{original.name}' on Google"
        button.href = f"https://www.google.com/?q={original.name}"

    @view()
    def select2_autocomplete(self, request):
        return JsonResponse({})

    @view(http_basic_auth=True)
    def api4(self, request):
        return HttpResponse("Basic Authentication allowed")

    @view(decorators=[csrf_exempt, xframe_options_sameorigin])
    def preview(self, request):
        if request.method == "POST":
            return HttpResponse("POST")
        return HttpResponse("GET")
            

```

#### Project Links


- Code: https://github.com/saxix/django-admin-extra-buttons
- Documentation: https://saxix.github.io/django-admin-extra-buttons/
- Issue Tracker: https://github.com/saxix/django-admin-extra-buttons/issues
- Download Package: https://pypi.org/project/django-admin-extra-buttons/
