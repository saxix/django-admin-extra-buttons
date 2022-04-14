import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_choice1(app, demomodel5, admin_user):
    url = reverse('admin:demo_demomodel5_changelist')
    res = app.get(url, user=admin_user)
    choice = res.pyquery('select[name=menu1]')
    option = choice.find('option')[1]

    res = app.get(option.attrib['value'], user=admin_user, auto_follow=True, extra_environ={'HTTP_REFERER': url})
    assert str(res.context['messages']._loaded_messages[0].message) == 'You have selected test1'


@pytest.mark.django_db
def test_choice2(app, demomodel5, admin_user):
    url = reverse('admin:demo_demomodel5_change', args=[demomodel5.pk])
    res = app.get(url, user=admin_user)
    choice = res.pyquery('select[name=menu2]')
    option = choice.find('option')[2]

    res = app.get(option.attrib['value'], user=admin_user, auto_follow=True, extra_environ={'HTTP_REFERER': url})
    assert res.request.path == f'/admin/demo/demomodel5/{demomodel5.pk}/test22/'
    assert str(res.context['messages']._loaded_messages[0].message) == f'You have selected test22 on {demomodel5}'
