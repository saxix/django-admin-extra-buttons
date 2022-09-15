from django.urls import reverse


def test_admin(app, admin_user):
    url = reverse('admin:demo_demomodel1_changelist')
    res = app.get(url, user=admin_user)
    assert res.status_code == 200
