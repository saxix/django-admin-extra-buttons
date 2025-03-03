 django-admin-extra-buttons
==========================


[![Pypi](https://badge.fury.io/py/django-admin-extra-buttons.svg)](https://badge.fury.io/py/django-admin-extra-buttons)
[![coverage](https://codecov.io/github/saxix/django-admin-extra-buttons/coverage.svg?branch=develop)](https://codecov.io/github/saxix/django-admin-extra-buttons?branch=develop)
[![Test](https://github.com/saxix/django-admin-extra-buttons/actions/workflows/test.yml/badge.svg)](https://github.com/saxix/django-admin-extra-buttons/actions/workflows/test.yml)
[![Documentation](https://github.com/saxix/django-admin-extra-buttons/actions/workflows/docs.yml/badge.svg)](https://saxix.github.io/django-admin-extra-buttons/)
[![Django](https://img.shields.io/pypi/frameworkversions/django/django-admin-extra-buttons)](https://pypi.org/project/django-admin-extra-buttons/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/django-admin-extra-buttons.svg)](https://pypi.org/project/django-admin-extra-buttons/)


![my image](https://saxix.github.io/django-admin-extra-buttons/images/screenshot.png)

This is a full rewriting of the original `django-admin-extra-url`. It
provides decorators to easily add custom buttons to Django Admin pages and/or add views to any ModelAdmin

It allows easy creation of wizards, actions and/or links to external resources
as well as api only views.

Four decorators are available:

- `@button()` to mark a method as extra view and show related button
- `@link()` This is used for "external" link, where you don't need to invoke local views.
- `@view()` View only decorator, this adds a new url but do not render any button.
- `@choice()` Menu like button, can be used to group multiple @views().


#### Project Links

- Code: https://github.com/saxix/django-admin-extra-buttons
- Documentation: https://saxix.github.io/django-admin-extra-buttons/
- Issue Tracker: https://github.com/saxix/django-admin-extra-buttons/issues
- Download Package: https://pypi.org/project/django-admin-extra-buttons/
