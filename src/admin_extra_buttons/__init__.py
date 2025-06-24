import django_stubs_ext

from .decorators import button, simple_button
from .handlers import ButtonHandler
from .mixins import ExtraButtonsMixin, LightweightButtonsMixin
from .version import __version__

NAME = "django-admin-extra-buttons"


VERSION = __version__

__all__ = [
    "__version__",
    "button",
    "simple_button",
    "ButtonHandler",
    "ExtraButtonsMixin",
    "LightweightButtonsMixin",
    "VERSION",
]
django_stubs_ext.monkeypatch()
