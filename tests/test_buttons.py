import pytest
from demo.models import DemoModel1, DemoModel2
from django.contrib.auth.models import Permission
from django.urls import reverse
from factory.django import DjangoModelFactory


class DemoModel1Factory(DjangoModelFactory):
    class Meta:
        model = DemoModel1


class DemoModel2Factory(DjangoModelFactory):
    class Meta:
        model = DemoModel2


@pytest.mark.django_db
def test_action(app, demomodel1, admin_user):
    url = reverse('admin:demo_demomodel1_change', args=[demomodel1.pk])
    res = app.get(url, user=admin_user)
    res = res.click(r'Update', index=0).follow()
    assert str(res.context['messages']._loaded_messages[0].message) == 'action called'


@pytest.mark.django_db
def test_action_no_response(app, demomodel1, admin_user):
    url = reverse('admin:demo_demomodel1_change', args=[demomodel1.pk])
    res = app.get(url, user=admin_user)
    res = res.click('No Response').follow()
    assert str(res.context['messages']._loaded_messages[0].message) == 'No_response_obj.'


def test_action_preserve_filters(django_app, admin_user):
    a, _, _ = DemoModel1Factory.create_batch(3)
    base_url = reverse('admin:demo_demomodel1_changelist')
    url = "%s?filter=on" % base_url
    res = django_app.get(url, user=admin_user)
    res = res.click('DemoModel1 #%s' % a.pk)
    link = res.pyquery('#btn-update')[0]
    assert link.get('href') == '/admin/demo/demomodel1/1/update/?_changelist_filters=filter%3Don'


def test_action_permission(app, staff_user):
    obj = DemoModel1Factory()
    perms = Permission.objects.filter(codename__in=['change_demomodel1'])
    staff_user.user_permissions.add(*perms)

    # try to by-pass button and call url directly as user with no permission
    url = reverse('admin:demo_demomodel1_update', args=[obj.pk])
    res = app.get(url, expect_errors=True)
    assert res.status_code == 403


@pytest.mark.django_db
def test_login_required(app):
    # try to by-pass button and call url directly as anonymous
    url = reverse('admin:demo_demomodel1_confirm')
    res = app.get(url, expect_errors=True)
    assert res.status_code == 403


def test_action_permission_callable(app, staff_user):
    obj = DemoModel1Factory()
    perms = Permission.objects.filter(codename__in=['change_demomodel1'])
    staff_user.user_permissions.add(*perms)

    url = reverse('admin:demo_demomodel1_change', args=[obj.pk])
    res = app.get(url, user=staff_user)
    assert not res.pyquery('#btn-update-callable-permission')

    url = reverse('admin:demo_demomodel1_update_callable_permission', args=[obj.pk])
    res = app.get(url, user=staff_user, expect_errors=True)
    assert res.status_code == 403


def test_visible_callable(app, admin_user, monkeypatch):
    url = reverse('admin:demo_demomodel1_changelist')
    res = app.get(url, user=admin_user)
    assert not res.pyquery('#btn-custom_visibile')

    monkeypatch.setenv('BTN_SHOW', '1')
    res = app.get(url, user=admin_user)
    assert res.pyquery('#btn-custom_visibile')


def test_disabled(app, admin_user):
    url = reverse('admin:demo_demomodel1_changelist')
    res = app.get(url, user=admin_user)
    assert res.pyquery('#btn-disabled.disabled')


def test_enabled(app, admin_user, monkeypatch):
    url = reverse('admin:demo_demomodel1_changelist')
    res = app.get(url, user=admin_user)
    assert res.pyquery('#btn-enabled.disabled')

    monkeypatch.setenv('BTN_ENABLED', '1')
    res = app.get(url, user=admin_user)
    assert not res.pyquery('#btn-enabled.disabled')
