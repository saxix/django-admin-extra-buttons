from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .handlers import ButtonHandler, ChoiceHandler, LinkHandler, ViewHandler

if TYPE_CHECKING:
    from collections.abc import Callable

    from .types import HandlerFunction


def button(**kwargs: Any) -> "Callable[[HandlerFunction], ButtonHandler]":
    def decorator(func: "HandlerFunction") -> ButtonHandler:
        return ButtonHandler(func=func, **kwargs)

    return decorator


def link(**kwargs: Any) -> "Callable[[HandlerFunction], LinkHandler]":
    def decorator(func: "HandlerFunction") -> LinkHandler:
        handler = LinkHandler(func=func, **kwargs)
        if not handler.single_object_invocation:  # pragma: no cover
            msg = f"'{func.__name__}' is decorated with @link() so it must accept one single argument of 'button'"
            raise TypeError(msg)
        return handler

    return decorator


def view(**kwargs: Any) -> "Callable[[HandlerFunction], ViewHandler]":
    def decorator(func: "HandlerFunction") -> ViewHandler:
        return ViewHandler(func=func, **kwargs)

    return decorator


def choice(**kwargs: Any) -> "Callable[[HandlerFunction], ChoiceHandler]":
    def decorator(func: "HandlerFunction") -> ChoiceHandler:
        return ChoiceHandler(func=func, **kwargs)

    return decorator
