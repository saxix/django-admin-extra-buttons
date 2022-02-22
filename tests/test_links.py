import logging

from django.contrib.auth.models import Permission
from django.urls import reverse

logger = logging.getLogger(__name__)


def test_link(django_app, staff_user):
    perms = Permission.objects.filter(codename__in=['change_demomodel2'])
    staff_user.user_permissions.add(*perms)
    url = reverse('admin:demo_demomodel2_changelist')
    res = django_app.get(url, user=staff_user)
    link = res.pyquery('#btn-google')[0]
    assert link.get('href') == 'https://www.google.com/'
