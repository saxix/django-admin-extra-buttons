import os

import django_webtest
import pytest
from demo.models import DemoModel1, DemoModel2, DemoModel5


def pytest_configure(config):
    os.environ['DEBUG'] = "False"


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
    return DemoModel2.objects.get_or_create(name='name1')[0]


@pytest.fixture
def demomodel1():
    return DemoModel1.objects.get_or_create(name='name1')[0]


@pytest.fixture
def demomodel5():
    return DemoModel5.objects.get_or_create(name='name1')[0]


@pytest.fixture(scope='function')
def staff_user(request, django_user_model, django_username_field):

    user, _ = django_user_model._default_manager.get_or_create(**{django_username_field: 'username',
                                                                  'is_staff': True})
    user.set_password('password')
    user.save()
    return user
