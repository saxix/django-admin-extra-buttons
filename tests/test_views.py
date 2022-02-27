import base64
import logging

from django.urls import reverse

logger = logging.getLogger(__name__)


def test_view(django_app, staff_user):
    url = reverse('admin:demo_demomodel3_api1')
    res = django_app.get(url, user=staff_user)
    assert res.content == b"OK"


def test_view_arg(django_app, staff_user):
    url = reverse('admin:demo_demomodel3_api2', args=[1])
    res = django_app.get(url, user=staff_user)
    assert res.content == b"1"


def test_anonymous(django_app, db):
    url = reverse('admin:demo_demomodel3_api3')
    res = django_app.get(url)
    assert res.content == b"Anonymous access allowed"


def test_basic_auth(django_app, staff_user):
    url = reverse('admin:demo_demomodel3_api4')
    res = django_app.get(url, expect_errors=True)
    assert res.status_code == 403

    credentials = f'{staff_user.username}:password'.encode()
    authorization = 'Basic %s' % base64.b64encode(credentials).decode("ascii")
    res = django_app.get(url, extra_environ=dict(HTTP_AUTHORIZATION=authorization))
    assert res.status_code == 200


def test_unknown_auth(django_app):
    url = reverse('admin:demo_demomodel3_api4')
    credentials = b'username:password'
    authorization = 'Site %s' % base64.b64encode(credentials).decode("ascii")
    res = django_app.get(url, expect_errors=True, extra_environ=dict(HTTP_AUTHORIZATION=authorization))
    assert res.status_code == 403
