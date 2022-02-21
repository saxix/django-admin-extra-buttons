import pytest
from django.core.exceptions import PermissionDenied

from admin_extra_buttons.templatetags.extra_buttons import default_if_empty
from admin_extra_buttons.utils import check_permission


@pytest.mark.parametrize("value,default,expected", (("a ", "", "a "),
                                                    ("", "a", "a"),
                                                    (" ", "a", "a"),
                                                    (None, "a", "a"),
                                                    ))
def test_default_if_empty(value, default, expected):
    assert default_if_empty(value, default) == expected
