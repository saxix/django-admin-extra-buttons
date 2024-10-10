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
    os.environ['DEBUG'] = "False"
    os.environ.update(DJANGO_SETTINGS_MODULE="demo.settings")

    import django

    django.setup()


@pytest.fixture(autouse=True)
def setup(settings):
    settings.AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']


@pytest.fixture(scope='function')
def app(request):
    wtm = django_webtest.WebTestMixin()
    wtm.csrf_checks = False
    wtm._patch_settings()
    request.addfinalizer(wtm._unpatch_settings)
    return django_webtest.DjangoTestApp()


@pytest.fixture
def demomodel2():
    from demo.models import DemoModel1, DemoModel2, DemoModel5
    return DemoModel2.objects.get_or_create(name='name1')[0]


@pytest.fixture
def demomodel1():
    from demo.models import DemoModel1, DemoModel2, DemoModel5
    return DemoModel1.objects.get_or_create(name='name1')[0]


@pytest.fixture
def demomodel5():
    from demo.models import DemoModel1, DemoModel2, DemoModel5
    return DemoModel5.objects.get_or_create(name='name1')[0]


@pytest.fixture(scope='function')
def staff_user(request, django_user_model, django_username_field):
    user, _ = django_user_model._default_manager.get_or_create(**{django_username_field: 'username',
                                                                  'is_staff': True})
    user.set_password('password')
    user.save()
    return user
