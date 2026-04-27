import base64
import logging
from unittest.mock import Mock

import pytest
from django.urls import reverse

from admin_extra_buttons.handlers import BaseExtraHandler, ChoiceHandler, LinkHandler, ViewHandler

logger = logging.getLogger(__name__)


def test_view(django_app, staff_user):
    url = reverse("admin:demo_demomodel3_api1")
    res = django_app.get(url, user=staff_user)
    assert res.content == b"OK"


def test_view_arg(django_app, staff_user):
    url = reverse("admin:demo_demomodel3_api2", args=[1])
    res = django_app.get(url, user=staff_user)
    assert res.content == b"1"


def test_anonymous(django_app, db):
    url = reverse("admin:demo_demomodel3_api3")
    res = django_app.get(url)
    assert res.content == b"Anonymous access allowed"


def test_basic_auth(django_app, staff_user):
    url = reverse("admin:demo_demomodel3_api4")
    res = django_app.get(url, expect_errors=True)
    assert res.status_code == 403

    credentials = f"{staff_user.username}:password".encode()
    authorization = "Basic %s" % base64.b64encode(credentials).decode("ascii")
    res = django_app.get(url, extra_environ={"HTTP_AUTHORIZATION": authorization})
    assert res.status_code == 200


def test_auth_handler(django_app, staff_user):
    url = reverse("admin:demo_demomodel3_api5")
    res = django_app.get(url, expect_errors=True)
    assert res.status_code == 403

    credentials = f"{staff_user.username}:password".encode()
    authorization = "Basic %s" % base64.b64encode(credentials).decode("ascii")
    res = django_app.get(url, extra_environ={"HTTP_AUTHORIZATION": authorization})
    assert res.status_code == 200


def test_unknown_auth(django_app):
    url = reverse("admin:demo_demomodel3_api4")
    credentials = b"username:password"
    authorization = "Site %s" % base64.b64encode(credentials).decode("ascii")
    res = django_app.get(url, expect_errors=True, extra_environ={"HTTP_AUTHORIZATION": authorization})
    assert res.status_code == 403


def test_view_handler_mutual_exclusion():
    with pytest.raises(ValueError, match="'http_basic_auth' and 'http_auth_handler' are mutually exclusive"):
        ViewHandler(lambda m, r: None, http_basic_auth=True, http_auth_handler=lambda r: None)


def test_link_handler_invoke():
    def func(ma, btn):
        pass

    handler = LinkHandler(func, href="http://example.com", label="Test")
    result = handler._invoke_handler(Mock(), Mock())
    assert result is None


def test_choice_handler_invoke():
    def func(ma, btn):
        pass

    handler = ChoiceHandler(func, href="http://example.com", label="Test", choices=[1, 2, 3])
    result = handler._invoke_handler(Mock(), Mock())
    assert result is None
