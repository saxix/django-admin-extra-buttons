from typing import Any, Protocol, TypeAlias, overload

from django.contrib.admin import ModelAdmin
from django.db.models import Model
from django.http import HttpRequest
from django.template import RequestContext

from .buttons import ButtonWidget, ChoiceButton, LinkButton
from .handlers import BaseExtraHandler, ButtonHandler, ChoiceHandler, LinkHandler

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

class HandlerFunction(Protocol):
    extra_buttons_handler: BaseExtraHandler
    __name__: str
    @overload
    def __call__(
        self, m: ModelAdmin[Any], request: HttpRequest, obj: Model | None = None, *args: Any, **kwargs: Any
    ) -> bool: ...
    @overload
    def __call__(self, m: ModelAdmin[Any], button: VisibleButton) -> bool: ...

HandlerWithButton: TypeAlias = ButtonHandler | LinkHandler | ChoiceHandler
