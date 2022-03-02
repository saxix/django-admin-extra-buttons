from unittest.mock import MagicMock

from demo.models import DemoModel1
from django.contrib.admin import site
from django.urls import reverse
from factory.django import DjangoModelFactory


class DemoModel1Factory(DjangoModelFactory):
    class Meta:
        model = DemoModel1


def test_get_common_context(db):
    obj = DemoModel1Factory()
    m = site._registry[DemoModel1]
    context = m.get_common_context(MagicMock(), obj.pk)
    assert context['original'] == obj


def test_error_message(app, admin_user, monkeypatch):
    url = reverse('admin:demo_demomodel1_changelist')
    res = app.get(url, user=admin_user)
    res = res.click('Error Message', index=0).follow()
    assert str(res.context['messages']._loaded_messages[0].message) == 'ZeroDivisionError: division by zero'
