from unittest.mock import MagicMock, Mock

from demo.models import DemoModel1
from django.contrib.admin import site
from django.urls import reverse
from factory.django import DjangoModelFactory

from admin_extra_buttons.handlers import BaseExtraHandler
from admin_extra_buttons.mixins import DummyAdminform, ExtraButtonsMixin


class DemoModel1Factory(DjangoModelFactory):
    class Meta:
        model = DemoModel1


def test_get_common_context(db):
    obj = DemoModel1Factory()
    m = site._registry[DemoModel1]
    context = m.get_common_context(MagicMock(), obj.pk)
    assert context["original"] == obj


def test_error_message(app, admin_user, monkeypatch):
    url = reverse("admin:demo_demomodel1_changelist")
    res = app.get(url, user=admin_user)
    res = res.click("Error Message", index=0).follow()
    assert str(res.context["messages"]._loaded_messages[0].message) == "ZeroDivisionError: division by zero"


def test_dummy_adminform_copy():
    original = DummyAdminform(foo="bar", baz=123)
    copied = original.__copy__()

    assert copied.foo == "bar"
    assert copied.baz == 123
    assert copied.prepopulated_fields == []


def test_dummy_adminform_iter():
    original = DummyAdminform(foo="bar")
    result = list(original)
    assert result == [None]


def test_dummy_adminform_init():
    df = DummyAdminform(foo="bar", hello="world")

    assert df.foo == "bar"
    assert df.hello == "world"
    assert df.prepopulated_fields == []


def test_base_handler_repr():
    def my_func(m, r):
        pass

    handler = BaseExtraHandler(my_func, model_admin=Mock())
    assert "my_func" in repr(handler)


def test_base_extra_handler_get_instance():
    def my_func(m, r):
        pass

    handler = BaseExtraHandler(my_func)
    new_handler = handler.get_instance(Mock())

    assert new_handler.func is my_func


def test_base_handler_single_object_invocation():
    def one_arg(m, pk):
        pass

    handler_one_arg = BaseExtraHandler(one_arg, model_admin=Mock())

    assert handler_one_arg.single_object_invocation is True


def test_base_handler_func_args():
    def my_handler(m, r, pk, extra=None):
        pass

    handler = BaseExtraHandler(my_handler, model_admin=Mock())
    args = handler.func_args

    assert "m" in args
    assert "r" in args
    assert "pk" in args
    assert "extra" in args


def test_extra_buttons_mixin_get_action_buttons():
    class TestMixin(ExtraButtonsMixin):
        pass

    mixin = TestMixin(Mock(), Mock())
    mock_context = MagicMock()

    result = mixin.get_action_buttons(mock_context)

    assert result == []


def test_extra_buttons_mixin_media():
    class TestMixin(ExtraButtonsMixin):
        pass

    from django.conf import settings

    original_debug = settings.DEBUG
    settings.DEBUG = True

    mixin = TestMixin(Mock(), Mock())
    media = mixin.media

    assert "admin_extra_buttons.js" in str(media)

    settings.DEBUG = original_debug


def test_extra_buttons_mixin_media_min():
    class TestMixin(ExtraButtonsMixin):
        pass

    from django.conf import settings

    original_debug = settings.DEBUG
    settings.DEBUG = False

    mixin = TestMixin(Mock(), Mock())
    media = mixin.media

    assert "admin_extra_buttons.min.js" in str(media)

    settings.DEBUG = original_debug


def test_extra_buttons_mixin_get_changeform_buttons():
    class TestMixin(ExtraButtonsMixin):
        pass

    mixin = TestMixin(Mock(), Mock())
    mock_context = MagicMock()

    result = mixin.get_changeform_buttons(mock_context)

    assert result == []


def test_extra_buttons_mixin_get_changelist_buttons():
    class TestMixin(ExtraButtonsMixin):
        pass

    mixin = TestMixin(Mock(), Mock())
    mock_context = MagicMock()

    result = mixin.get_changelist_buttons(mock_context)

    assert result == []
