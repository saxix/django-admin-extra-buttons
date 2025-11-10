from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .handlers import ButtonHandler, ChoiceHandler, LinkHandler, ViewHandler

if TYPE_CHECKING:
    from collections.abc import Callable

    from .types import (
        ButtonHandlerFunction,
        ChoiceHandlerFunction,
        LinkHandlerFunction,
        ViewHandlerFunction,
    )


def button(**kwargs: Any) -> "Callable[[ButtonHandlerFunction], ButtonHandler]":
    def decorator(func: "ButtonHandlerFunction") -> ButtonHandler:
        return ButtonHandler(func=func, **kwargs)

    return decorator


def link(**kwargs: Any) -> "Callable[[LinkHandlerFunction], LinkHandler]":
    def decorator(func: "LinkHandlerFunction") -> LinkHandler:
        handler = LinkHandler(func=func, **kwargs)
        if not handler.single_object_invocation:  # pragma: no cover
            msg = f"'{func.__name__}' is decorated with @link() so it must accept one single argument of 'button'"
            raise TypeError(msg)
        return handler

    return decorator


def view(**kwargs: Any) -> "Callable[[ViewHandlerFunction], ViewHandler]":
    def decorator(func: "ViewHandlerFunction") -> ViewHandler:
        return ViewHandler(func=func, **kwargs)

    return decorator


def choice(**kwargs: Any) -> "Callable[[ChoiceHandlerFunction], ChoiceHandler]":
    def decorator(func: "ChoiceHandlerFunction") -> ChoiceHandler:
        return ChoiceHandler(func=func, **kwargs)

    return decorator
