from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar

from .handlers import ButtonHandler, ChoiceHandler, LinkHandler, ViewHandler

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable

    from .mixins import ExtraButtonsMixin
    from .types import (
        ButtonHandlerFunction,
        ChoiceHandlerFunction,
        LinkHandlerFunction,
        ViewHandlerFunction,
        VisibleButton,
    )

_S = TypeVar("_S", bound="ExtraButtonsMixin")
_B = TypeVar("_B", bound="VisibleButton")


def button(**kwargs: Any) -> Callable[[ButtonHandlerFunction[_S]], ButtonHandler]:
    def decorator(func: ButtonHandlerFunction[_S]) -> ButtonHandler:
        return ButtonHandler(func=func, **kwargs)

    return decorator


def link(**kwargs: Any) -> Callable[[LinkHandlerFunction[_S, _B]], LinkHandler]:
    def decorator(func: LinkHandlerFunction[_S, _B]) -> LinkHandler:
        handler = LinkHandler(func=func, **kwargs)
        if len(handler.func_args) == 1:  # pragma: no cover
            msg = f"'{func.__name__}' is decorated with @link() so it must accept one single argument of 'button'"
            raise TypeError(msg)
        return handler

    return decorator


def view(**kwargs: Any) -> Callable[[ViewHandlerFunction[_S]], ViewHandler]:
    def decorator(func: ViewHandlerFunction[_S]) -> ViewHandler:
        return ViewHandler(func=func, **kwargs)

    return decorator


def choice(**kwargs: Any) -> Callable[[ChoiceHandlerFunction[_S, _B]], ChoiceHandler]:
    def decorator(func: ChoiceHandlerFunction[_S, _B]) -> ChoiceHandler:
        return ChoiceHandler(func=func, **kwargs)

    return decorator
