from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

from .handlers import ButtonHandler, ChoiceHandler, LinkHandler, ViewHandler

if TYPE_CHECKING:
    from .types import HandlerFunction, LinkHandlerFunction


def button(
    html_attrs: dict[str, Any] | None = None,
    change_list: bool | None = None,
    change_form: bool | None = None,
) -> Callable[[Callable], ButtonHandler]:
    """
    Decorator that turns a ModelAdmin method into an admin button.

    Args:
        html_attrs: A dict of HTML attributes for the button's <a> tag.
        change_list: If True, show the button on the changelist page.
        change_form: If True, show the button on the change form page.
    """

    def decorator(func: Callable) -> ButtonHandler:
        return ButtonHandler(
            func=func,
            html_attrs=html_attrs,
            change_list=change_list,
            change_form=change_form,
        )

    return decorator


def simple_button(
    html_attrs: dict | None = None,
    change_list: bool | None = None,
    change_form: bool | None = None,
) -> Callable[[Callable], ButtonHandler]:
    """An alias for the @button decorator for convenience."""
    return button(
        html_attrs=html_attrs, change_list=change_list, change_form=change_form
    )


def link(**kwargs: Any) -> "Callable[[LinkHandlerFunction], LinkHandler]":
    def decorator(func: "LinkHandlerFunction") -> LinkHandler:
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


__all__ = ["button", "simple_button"]
