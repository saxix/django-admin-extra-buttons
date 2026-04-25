from typing import Any, Callable, Protocol, TypeAlias, TypeVar

import typing_extensions
from django.db.models import Model
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext

from .buttons import ChoiceButton, LinkButton, StandardButton
from .handlers import BaseExtraHandler, ButtonHandler, ChoiceHandler, LinkHandler
from .mixins import ExtraButtonsMixin

_S = TypeVar("_S", bound=ExtraButtonsMixin)
_B = TypeVar("_B", bound=VisibleButton)

VisibleButton: TypeAlias = StandardButton | LinkButton | ChoiceButton

class PermissionHandler(Protocol):
    def __call__(
        self, request: HttpRequest, obj: Model | None = None, handler: BaseExtraHandler | None = None
    ) -> bool: ...

class WidgetProtocol(Protocol):
    button_class: StandardButton
    change_list: bool
    change_form: bool

    def get_button_params(self, context: RequestContext, **extra: Any) -> dict[str, Any]: ...
    def get_button(self, context: RequestContext) -> VisibleButton: ...

class BaseHandlerFunction(Protocol):
    __name__: str
    extra_buttons_handler: BaseExtraHandler

Callback1: TypeAlias = Callable[[_S, HttpRequest], HttpResponse | None]
Callback2: TypeAlias = Callable[[_S, HttpRequest, str], HttpResponse | None]

ViewHandlerFunction: TypeAlias = Callback1[_S] | Callback2[_S]
ButtonHandlerFunction: typing_extensions.TypeAlias = ViewHandlerFunction[_S]

ChoiceHandlerFunction: TypeAlias = Callable[[_S, _B], HttpResponse | None]
LinkHandlerFunction: TypeAlias = Callable[[_S, _B], HttpResponse | None]

GenericHandler: TypeAlias = (
    ButtonHandlerFunction[Any]
    | ViewHandlerFunction[Any]
    | ChoiceHandlerFunction[Any, Any]
    | LinkHandlerFunction[Any, Any]
)

HandlerWithButton: TypeAlias = ButtonHandler | LinkHandler | ChoiceHandler
