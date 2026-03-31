from collections.abc import Callable
from typing import Any, Protocol

from django.db.models import Model
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext

from .buttons import ButtonWidget, ChoiceButton, LinkButton
from .handlers import BaseExtraHandler, ButtonHandler, ChoiceHandler, LinkHandler
from .mixins import ExtraButtonsMixin

type VisibleButton = ButtonWidget | LinkButton | ChoiceButton

class PermissionHandler(Protocol):
    def __call__(
        self, request: HttpRequest, obj: Model | None = None, handler: BaseExtraHandler | None = None
    ) -> bool: ...

class WidgetProtocol(Protocol):
    button_class: ButtonWidget
    change_list: bool
    change_form: bool

    def get_button_params(self, context: RequestContext, **extra: Any) -> dict[str, Any]: ...
    def get_button(self, context: RequestContext) -> ButtonWidget: ...

class BaseHandlerFunction(Protocol):
    __name__: str
    extra_buttons_handler: BaseExtraHandler

"""
# xxx1 = Callable[[ExtraButtonsMixin, HttpRequest], HttpResponse | None]
# xxx2 = Callable[[ExtraButtonsMixin, HttpRequest, str], HttpResponse | None]
#
# aaa = xxx1 | xxx2
#
# bbb = Callable[[ExtraButtonsMixin, VisibleButton], HttpResponse | None]
#
# zzz = aaa | bbb
#
# ViewHandlerFunction = aaa
# ButtonHandlerFunction = aaa
# ChoiceHandlerFunction = bbb
# LinkHandlerFunction = bbb
"""

type Callback1 = Callable[[ExtraButtonsMixin, HttpRequest], HttpResponse | None]
type Callback2 = Callable[[ExtraButtonsMixin, HttpRequest, str], HttpResponse | None]

type ViewHandlerFunction = Callback1 | Callback2
ButtonHandlerFunction = ViewHandlerFunction

type ChoiceHandlerFunction = Callable[[ExtraButtonsMixin, VisibleButton], HttpResponse | None]
type LinkHandlerFunction = Callable[[ExtraButtonsMixin, VisibleButton], HttpResponse | None]

type GenericHandler = ButtonHandlerFunction | ViewHandlerFunction | ChoiceHandlerFunction | LinkHandlerFunction

type HandlerWithButton = ButtonHandler | LinkHandler | ChoiceHandler
