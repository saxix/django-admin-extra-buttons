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
