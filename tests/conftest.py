import os
import sys
from pathlib import Path

import django_webtest
import pytest

here = Path(__file__).parent
DEMOAPP_PATH = here / "demoapp"
sys.path.insert(0, str(here / "../src"))
sys.path.insert(0, str(DEMOAPP_PATH))


def pytest_configure(config):
    os.environ["DEBUG"] = "False"
    os.environ.update(DJANGO_SETTINGS_MODULE="demo.settings")

    import django

    # Python 3.14 and Django 4.2 have a conflict in Context.__copy__
    # triggered by instrumented_test_render.
    if sys.version_info >= (3, 14) and django.VERSION < (5, 0):
        from django.template import context

        def __copy__(self):
            # We must return a new instance that behaves like a Context
            # and contains the same data, but avoids the broken super().__copy__()
            cls = self.__class__
            result = cls.__new__(cls)
            # Copy dictionaries
            result.dicts = self.dicts[:]
            # Copy other attributes that might be needed by Django
            for attr in ("render_context", "template", "autoescape", "use_l10n", "use_tz"):
                if hasattr(self, attr):
                    setattr(result, attr, getattr(self, attr))
            return result

        context.BaseContext.__copy__ = __copy__

    django.setup()


@pytest.fixture(autouse=True)
def setup(settings):
    settings.AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]


@pytest.fixture(scope="function")
def app(django_app_factory):
    return django_app_factory(csrf_checks=False)
    # wtm = django_webtest.WebTestMixin()
    # wtm.csrf_checks = False
    # wtm._patch_settings()
    # request.addfinalizer(wtm._unpatch_settings)
    # return django_webtest.DjangoTestApp()


@pytest.fixture
def demomodel2():
    from demo.models import DemoModel2

    return DemoModel2.objects.get_or_create(name="name1")[0]


@pytest.fixture
def demomodel1():
    from demo.models import DemoModel1

    return DemoModel1.objects.get_or_create(name="name1")[0]


@pytest.fixture
def demomodel5():
    from demo.models import DemoModel5

    return DemoModel5.objects.get_or_create(name="name1")[0]


@pytest.fixture(scope="function")
def staff_user(request, django_user_model, django_username_field):
    user, _ = django_user_model._default_manager.get_or_create(**{django_username_field: "username", "is_staff": True})
    user.set_password("password")
    user.save()
    return user
