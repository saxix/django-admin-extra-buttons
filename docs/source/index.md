# django-admin-extra-buttons


[![Pypi](https://badge.fury.io/py/django-admin-extra-buttons.svg)](https://badge.fury.io/py/django-admin-extra-buttons)
[![coverage](https://codecov.io/github/saxix/django-admin-extra-buttons/coverage.svg?branch=develop)](https://codecov.io/github/saxix/django-admin-extra-buttons?branch=develop)
[![Test](https://github.com/saxix/django-admin-extra-buttons/actions/workflows/test.yml/badge.svg)](https://github.com/saxix/django-admin-extra-buttons/actions/workflows/test.yml)
[![ReadTheDocs](https://readthedocs.org/projects/django-admin-extra-buttons/badge/?version=latest)](https://django-admin-extra-buttons.readthedocs.io/en/latest/)


![Buttons](./images/screenshot.png)

This is a full rewriting of the original `django-admin-extra-url`. It
provides decorators to easily add custom buttons to Django Admin pages.

Will be possible to create wizards, actions and/or link to external resources
as well as api only views.

It provides 3 decorators:

- [@button()](api/button.md) to mark a method as extra view and show related button
- [@link()](api/link.md) This is used for "external" link, where you don't need to invoke local views.
- [@view()](api/view.md) View only decorator, this adds a new url but do not render any button.

Install
-------

    pip install django-admin-extra-buttons


After installation add it to ``INSTALLED_APPS``

    INSTALLED_APPS = (
       ...
       'admin_extra_buttons',
    )

