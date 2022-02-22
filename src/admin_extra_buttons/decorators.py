from .handlers import ButtonHandler, LinkHandler, ViewHandler


def button(**kwargs):
    def decorator(func):
        return ButtonHandler(func, **kwargs)

    return decorator


def link(**kwargs):
    def decorator(func):
        handler = LinkHandler(func, **kwargs)
        if len(handler.sig.parameters) != 2: # pragma: no cover
            raise TypeError(
                "'%s' is decorated with @link() so it must "
                "accept one single argument of 'button'" % func.__name__)
        return handler

    return decorator


def view(**kwargs):
    def decorator(func):
        return ViewHandler(func, **kwargs)

    return decorator
