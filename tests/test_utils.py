import pytest
from django.core.exceptions import PermissionDenied

from admin_extra_buttons.utils import check_permission


def test_check_permission(rf, staff_user, admin_user):
    request = rf.get('/')
    request.user = staff_user
    with pytest.raises(PermissionDenied):
        check_permission('demo_add_demomodel1', request)

    with pytest.raises(PermissionDenied):
        check_permission(lambda r, o: False, request)

    request.user = admin_user
    assert check_permission('demo_add_demomodel1', request)
    assert check_permission(lambda r, o: True, request)
