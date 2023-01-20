import ast
import codecs
import inspect
from urllib.parse import urlencode

from django.conf import settings
from django.core.checks import Warning
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect


def handle_basic_auth(request):
    from django.contrib.auth import authenticate, login
    if "HTTP_AUTHORIZATION" in request.META:
        authmeth, auth = request.META["HTTP_AUTHORIZATION"].split(" ", 1)
        if authmeth.lower() == "basic":
            auth = codecs.decode(auth.encode("utf8").strip(), "base64").decode()
            username, password = auth.split(":", 1)
            user = authenticate(request=request, username=username, password=password)
            if user:  # pragma: no branch
                login(request, user)
                return user
    raise PermissionDenied()


def get_preserved_filters(request, **extras):
    filters = request.GET.get('_changelist_filters', '')
    if filters:
        preserved_filters = request.GET.get('_changelist_filters')
    else:
        preserved_filters = request.GET.urlencode()

    if preserved_filters:
        return urlencode({'_changelist_filters': preserved_filters})
    return ''


def labelize(label):
    return label.replace('_', ' ').strip().title()


def check_permission(handler, permission, request, obj=None):
    if callable(permission):
        if not permission(request, obj, handler=handler):
            raise PermissionDenied
    elif not request.user.has_perm(permission):
        raise PermissionDenied
    return True


class HttpResponseRedirectToReferrer(HttpResponseRedirect):
    def __init__(self, request, *args, **kwargs):
        redirect_to = request.META.get('HTTP_REFERER', '/')
        # redirect_to = request.META.get('HTTP_REFERER', reverse("admin:index"))
        super().__init__(redirect_to, *args, **kwargs)


def get_all_permissions():
    from django.contrib.auth.models import Permission
    return [f'{p[0]}.{p[1]}'
            for p in (Permission.objects
                      .select_related('content_type')
                      .values_list('content_type__app_label', 'codename'))]


def check_decorator_errors(cls):
    target = cls
    standard_permissions = []
    errors = []
    if 'django.contrib.auth' in settings.INSTALLED_APPS:  # pragma: no branch
        standard_permissions = get_all_permissions()

    def visit_FunctionDef(node):
        # deco = []
        for n in node.decorator_list:
            if isinstance(n, ast.Call):
                name = n.func.attr if isinstance(n.func, ast.Attribute) else n.func.id
            else:
                name = n.attr if isinstance(n, ast.Attribute) else n.id
            if name in ['button', 'view']:
                if standard_permissions:  # pragma: no branch
                    for k in n.keywords:
                        if k.arg == 'permission' and isinstance(k.value, ast.Constant):
                            perm_name = k.value.value
                            if perm_name not in standard_permissions:
                                errors.append(Warning(f'"{cls.__name__}.{node.name}" '
                                                      f'is checking for a non existing permission '
                                                      f'"{perm_name}"',
                                                      id='admin_extra_buttons.PERM', ))

    node_iter = ast.NodeVisitor()
    node_iter.visit_FunctionDef = visit_FunctionDef
    node_iter.visit(ast.parse(inspect.getsource(target)))
    return errors
