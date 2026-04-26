import pytest
from unittest.mock import MagicMock, Mock

from admin_extra_buttons.templatetags.extra_buttons import (
    default_if_empty,
    get_action_buttons,
    get_changeform_buttons,
    get_changelist_buttons,
)


@pytest.mark.parametrize(
    "value,default,expected",
    (
        ("a ", "", "a "),
        ("", "a", "a"),
        (" ", "a", "a"),
        (None, "a", "a"),
    ),
)
def test_default_if_empty(value, default, expected):
    assert default_if_empty(value, default) == expected


def test_default_if_empty_with_value():
    result = default_if_empty("hello", "default")
    assert result == "hello"


def test_default_if_empty_with_whitespace():
    result = default_if_empty("   ", "default")
    assert result == "default"


def test_templatetags_get_action_buttons_no_method():
    from django.template import RequestContext

    model_admin = Mock()
    del model_admin.get_action_buttons
    context = MagicMock(spec=RequestContext)

    result = get_action_buttons(context, model_admin)

    assert result == []


def test_templatetags_get_changeform_buttons_no_method():
    from django.template import RequestContext

    model_admin = Mock()
    del model_admin.get_changeform_buttons
    context = MagicMock(spec=RequestContext)

    result = get_changeform_buttons(context, model_admin)

    assert result == []


def test_templatetags_get_changelist_buttons_no_method():
    from django.template import RequestContext

    model_admin = Mock()
    del model_admin.get_changelist_buttons
    context = MagicMock(spec=RequestContext)

    result = get_changelist_buttons(context, model_admin)

    assert result == []
