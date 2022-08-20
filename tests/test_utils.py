import pytest
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from admin_extra_buttons.decorators import button
from admin_extra_buttons.utils import check_decorator_errors, check_permission


def test_check_permission(rf, staff_user, admin_user):
    request = rf.get('/')
    request.user = staff_user
    with pytest.raises(PermissionDenied):
        check_permission(None, 'demo_add_demomodel1', request)

    with pytest.raises(PermissionDenied):
        check_permission(None, lambda r, o, **kw: False, request)

    request.user = admin_user
    assert check_permission(None, 'demo_add_demomodel1', request)
    assert check_permission(None, lambda r, o, **kw: True, request)


class Class1:
    @button(permission="invalid")
    def bbb(self):
        pass


class Class2:
    @button(permission="auth.add_user")
    def bbb(self):
        pass

    @login_required
    def aaa(self):
        pass


@pytest.mark.django_db
@pytest.mark.parametrize("cls, expected", ((Class1, 1), (Class2, 0)))
def test_check_decorator_errors(cls, expected):
    errors = check_decorator_errors(cls)
    assert len(errors) == expected, errors
