from unittest.mock import MagicMock

from admin_extra_buttons.buttons import Button, LinkButton
from admin_extra_buttons.handlers import ButtonHandler, LinkHandler


def test_button_visibility():
    def v(btn):
        return isinstance(btn, Button)

    h = ButtonHandler(MagicMock(__name__="a"), visible=v)
    btn: Button = h.get_button({"a": 1})
    assert bool(btn.visible)


def test_link_visibility():
    def v(btn):
        return isinstance(btn, LinkButton)

    h = LinkHandler(MagicMock(__name__="a"), visible=v)
    btn: LinkButton = h.get_button({"a": 1})
    assert bool(btn.visible)
