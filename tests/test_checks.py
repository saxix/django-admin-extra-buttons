from admin_extra_buttons.utils import check_decorator_errors
from demo.admin import Admin1


def test_permissions(db):
    check_decorator_errors(Admin1)
