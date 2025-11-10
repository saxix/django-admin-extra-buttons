from typing import Any, Callable, Protocol, TypeAlias

from django.db.models import Model
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext

from .buttons import ButtonWidget, ChoiceButton, LinkButton
from .handlers import BaseExtraHandler, ButtonHandler, ChoiceHandler, LinkHandler
from .mixins import ExtraButtonsMixin

VisibleButton: TypeAlias = ButtonWidget | LinkButton | ChoiceButton

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

Callback1: TypeAlias = Callable[[ExtraButtonsMixin, HttpRequest], HttpResponse | None]
Callback2: TypeAlias = Callable[[ExtraButtonsMixin, HttpRequest, str], HttpResponse | None]

ViewHandlerFunction: TypeAlias = Callback1 | Callback2
ButtonHandlerFunction = ViewHandlerFunction

ChoiceHandlerFunction: TypeAlias = Callable[[ExtraButtonsMixin, VisibleButton], HttpResponse | None]
LinkHandlerFunction: TypeAlias = Callable[[ExtraButtonsMixin, VisibleButton], HttpResponse | None]

GenericHandler: TypeAlias = ButtonHandlerFunction | ViewHandlerFunction | ChoiceHandlerFunction | LinkHandlerFunction

HandlerWithButton: TypeAlias = ButtonHandler | LinkHandler | ChoiceHandler
