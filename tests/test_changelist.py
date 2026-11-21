import pytest
from django.contrib.auth.models import Permission
from django.urls import reverse


@pytest.mark.parametrize("can_add", [False, True])
def test_changelist_add_link_follows_permission(app, staff_user, can_add):
    permissions = ["view_demomodel1"]
    if can_add:
        permissions.append("add_demomodel1")
    staff_user.user_permissions.add(
        *Permission.objects.filter(content_type__app_label="demo", codename__in=permissions)
    )

    response = app.get(reverse("admin:demo_demomodel1_changelist"), user=staff_user)
    add_links = response.pyquery(".object-tools a.addlink")

    assert response.pyquery(".object-tools #btn-custom_path")
    if can_add:
        assert add_links.attr("href") == reverse("admin:demo_demomodel1_add")
    else:
        assert not add_links
