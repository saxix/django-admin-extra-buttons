from collections.abc import Callable
from typing import Any, Protocol

from django.db.models import Model
from django.http import HttpRequest, HttpResponse, StreamingHttpResponse
from django.template import RequestContext

from .buttons import ChoiceButton, LinkButton, StandardButton
from .handlers import BaseExtraHandler, ButtonHandler, ChoiceHandler, LinkHandler
from .mixins import ExtraButtonsMixin

type HttpResponseLike = HttpResponse | StreamingHttpResponse

type VisibleButton = StandardButton | LinkButton | ChoiceButton

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

type Callback1[_S: ExtraButtonsMixin] = Callable[[_S, HttpRequest], HttpResponseLike | None]
type Callback2[_S: ExtraButtonsMixin] = Callable[[_S, HttpRequest, str], HttpResponseLike | None]

type ViewHandlerFunction[_S: ExtraButtonsMixin] = Callback1[_S] | Callback2[_S]
type ButtonHandlerFunction[_S: ExtraButtonsMixin] = ViewHandlerFunction[_S]

type ChoiceHandlerFunction[_S: ExtraButtonsMixin, _B: VisibleButton] = Callable[[_S, _B], HttpResponseLike | None]
type LinkHandlerFunction[_S: ExtraButtonsMixin, _B: VisibleButton] = Callable[[_S, _B], HttpResponseLike | None]

type GenericHandler = (
    ButtonHandlerFunction[Any]
    | ViewHandlerFunction[Any]
    | ChoiceHandlerFunction[Any, Any]
    | LinkHandlerFunction[Any, Any]
)

type HandlerWithButton = ButtonHandler | LinkHandler | ChoiceHandler
