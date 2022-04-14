from demo.admin import Admin1
from demo.models import DemoModel1
from django.contrib.admin import site

from admin_extra_buttons.utils import check_decorator_errors


def test_permissions(db):
    assert check_decorator_errors(Admin1) == []


def test_mixin_checks(db):
    model_admin = site._registry[DemoModel1]
    assert model_admin.check() == []
