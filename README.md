django-admin-extra-buttons
==========================


[![Pypi](https://badge.fury.io/py/django-admin-extra-buttons.svg)](https://badge.fury.io/py/django-admin-extra-buttons)
[![coverage](https://codecov.io/github/saxix/django-admin-extra-buttons/coverage.svg?branch=develop)](https://codecov.io/github/saxix/django-admin-extra-buttons?branch=develop)
[![Test](https://github.com/saxix/django-admin-extra-buttons/actions/workflows/test.yml/badge.svg)](https://github.com/saxix/django-admin-extra-buttons/actions/workflows/test.yml)

[comment]: <> ([![ReadTheDocs]&#40;https://readthedocs.org/projects/django-admin-extra-buttons/badge/?version=latest&#41;]&#40;https://django-admin-extra-buttons.readthedocs.io/en/latest/&#41;)

[![Docs](https://github.com/saxix/django-admin-extra-buttons/actions/workflows/docs.yml/badge.svg)](https://github.com/saxix/django-admin-extra-buttons/actions/workflows/docs.yml)

![Buttons](./docs/source/images/screenshot.png)


This is a full rewriting of the original `django-admin-extra-url`. It
provides decorators to easily add custom buttons to Django Admin pages.

It allows to create wizards, actions and/or links to external resources 
as well as api only views.

It provides 3 decorators: 

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

    from admin_extra_buttons.api import ExtraButtonsMixin, button, link, view

    class MyModelModelAdmin(extras.ExtraButtonsMixin, admin.ModelAdmin):

        @link(label='Search On Google', change_form=True, change_list=False)
        def search_on_google(self, button):
            obj = button.context['original']
            button.href = f'http://www.google.com?q={obj.name}'

        @button() # /admin/myapp/mymodel/update_all/
        def consolidate(self, request):
            ...
            ...

        @button() # /admin/myapp/mymodel/update/10/
        def update(self, request, pk):
            # if we use `pk` in the args, the button will be in change_form
            obj = self.get_object(request, pk)
            ...

        @button(permission=lambda request, obj: request.user.is_superuser)
        def empty_table(self, request):
            if request.method == 'POST':
                self.model.objects.all().delete()
            else:
                return extras._confirm_action(self, request, self.truncate,
                                       'Continuing will erase the entire content of the table.',
                                       'Successfully executed', )
