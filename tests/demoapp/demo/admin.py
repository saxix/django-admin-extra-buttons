import os
from typing import TYPE_CHECKING, Any

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.contrib.auth.decorators import login_required
from django.db.models import Model, QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.safestring import SafeString

from admin_extra_buttons.api import ExtraButtonsMixin, button, choice, confirm_action, link, view
from admin_extra_buttons.buttons import ChoiceButton, LinkButton, StandardButton
from admin_extra_buttons.utils import handle_basic_auth

from .models import DemoModel1, DemoModel2, DemoModel3, DemoModel4, DemoModel5
from .upload import UploadMixin

if TYPE_CHECKING:
    from admin_extra_buttons.types import HandlerWithButton, VisibleButton


class TestFilter(SimpleListFilter):
    parameter_name = "filter"
    title = "Dummy filter for testing"

    def lookups(self, request: HttpRequest, model_admin: admin.ModelAdmin[Model]) -> tuple[tuple[str, str], ...]:
        return (
            ("on", "On"),
            ("off", "Off"),
        )

    def queryset(self, request: HttpRequest, queryset: QuerySet[Model]) -> QuerySet[Model]:
        return queryset


# start docs here
class Admin1(ExtraButtonsMixin, admin.ModelAdmin[DemoModel1]):
    list_filter = [TestFilter]

    @button(permission="demo.add_demomodel1", change_form=True, change_list=False, html_attrs={"class": "aeb-green"})
    def refresh(self: ExtraButtonsMixin, request: HttpRequest) -> None:
        self.message_user(request, "refresh called")

    @button(label="Refresh", permission=lambda request, object, **kw: False)
    def refresh_callable(self: ExtraButtonsMixin, request: HttpRequest) -> HttpResponseRedirect:
        opts = self.model._meta
        self.message_user(request, "refresh called")
        return HttpResponseRedirect(reverse(admin_urlname(opts, SafeString("changelist"))))

    @button(pattern="a/b/")
    def custom_path(self: ExtraButtonsMixin, request: HttpRequest) -> HttpResponseRedirect:
        opts = self.model._meta
        self.message_user(request, "You invoked `custom_path` linked to 'a/b/' url ")
        return HttpResponseRedirect(reverse(admin_urlname(opts, SafeString("changelist"))))

    @button(html_attrs={"style": "background-color:#EDD372;color:black"})
    def no_response(self: ExtraButtonsMixin, request: HttpRequest) -> None:
        self.message_user(request, "No Response provided.")

    @button(html_attrs={"style": "background-color:#DC6C6C;color:black"})
    def confirm(self: ExtraButtonsMixin, request: HttpRequest) -> HttpResponse:
        def _action(request: HttpRequest) -> None:
            pass

        return confirm_action(
            self,
            request,
            _action,
            message="Confirm action",
            success_message="Successfully executed",
        )

    @button(permission="demo.delete_demomodel1")
    def update(self: ExtraButtonsMixin, request: HttpRequest, pk: str) -> HttpResponseRedirect:
        opts = self.model._meta
        self.message_user(request, "action called")
        return HttpResponseRedirect(reverse(admin_urlname(opts, SafeString("changelist"))))

    @button()
    def no_response_single(self: ExtraButtonsMixin, request: HttpRequest, object_id: str) -> None:
        self.message_user(request, "No_response_obj.")

    @button(permission=lambda request, obj, **kw: False)
    def update_callable_permission(
        self: ExtraButtonsMixin, request: HttpRequest, object_id: str
    ) -> HttpResponseRedirect:
        opts = self.model._meta
        self.message_user(request, "action called")
        return HttpResponseRedirect(reverse(admin_urlname(opts, SafeString("changelist"))))

    @button(pattern="a/b/<path:object_id>")
    def custom_update(self: ExtraButtonsMixin, request: HttpRequest, object_id: str) -> HttpResponseRedirect:
        opts = self.model._meta
        self.message_user(request, "action called")
        return HttpResponseRedirect(reverse(admin_urlname(opts, SafeString("changelist"))))

    @button(visible=lambda btn: "BTN_SHOW" in os.environ)
    def custom_visibile(self: ExtraButtonsMixin, request: HttpRequest) -> None:
        pass

    #
    @button(enabled=False)
    def disabled(self: ExtraButtonsMixin, request: HttpRequest) -> None:
        pass

    @button(enabled=lambda btn: "BTN_ENABLED" in os.environ)
    def enabled(self: ExtraButtonsMixin, request: HttpRequest) -> None:
        pass

    @link(href="https://www.google.com/", visible=lambda btn: True, permissions=["auth.view_user"])
    def invisible(self: ExtraButtonsMixin, btn: "StandardButton") -> None:
        btn.visible = False

    @button()
    def error_message(self: ExtraButtonsMixin, request: HttpRequest) -> None:
        try:
            1 / 0
        except Exception as e:  # noqa: BLE001
            self.message_error_to_user(request, e)


class Admin2(ExtraButtonsMixin, admin.ModelAdmin[DemoModel2]):
    @link(href="https://www.google.com/", change_form=False, html_attrs={"target": "_new"})
    def google(self: ExtraButtonsMixin, btn: "VisibleButton") -> None:
        pass

    @link(href=None, change_list=False, html_attrs={"target": "_new", "style": "background-color:var(--button-bg)"})
    def search_on_google(self: ExtraButtonsMixin, btn: "VisibleButton") -> None:
        original = btn.context["original"]
        btn.label = f"Search '{original.name}' on Google"
        btn.href = f"https://www.google.com/?q={original.name}"


    @link(href="/", visible=lambda btn: "BTN_SHOW2" in os.environ, change_list=True)
    def custom_visibile(self: ExtraButtonsMixin, btn:"VisibleButton") -> None:
        pass


class Admin3(ExtraButtonsMixin, admin.ModelAdmin[DemoModel3]):
    @view()
    def api1(self: ExtraButtonsMixin, request:HttpRequest) -> HttpResponse:
        return HttpResponse("OK")

    @view(permissions=["demo.view_demomodel3"])
    def api2(self: ExtraButtonsMixin, request: HttpRequest, pk: str) -> HttpResponse:
        return HttpResponse(pk)

    @view(login_required=False)
    def api3(self: ExtraButtonsMixin, request:HttpRequest) -> HttpResponse:
        return HttpResponse("Anonymous access allowed")

    @view(http_basic_auth=True)
    def api4(self: ExtraButtonsMixin, request:HttpRequest) -> HttpResponse:
        return HttpResponse("Basic Authentication allowed")

    @view(http_auth_handler=handle_basic_auth)
    def api5(self: ExtraButtonsMixin, request:HttpRequest) -> HttpResponse:
        return HttpResponse("Basic Authentication allowed")


class Admin4(UploadMixin, admin.ModelAdmin[DemoModel4]):
    upload_handler = lambda *args: [1, 2, 3]


class Admin5(ExtraButtonsMixin, admin.ModelAdmin[DemoModel5]):
    list_filter = [TestFilter]

    @choice(change_list=True, permission=["auth.view_user"])
    def _menu1(self, btn: "ChoiceButton") -> None:
        btn.choices = [self.test1, self.test2, self.test21]
        btn.label = "Menu #1"

    @choice(change_list=False, change_form=True, label="Menu Advanced")
    def _menu_adv(self, btn: ChoiceButton) -> None:
        btn.visible = True
        obj: DemoModel5 = btn.original  # type: ignore[assignment]
        if obj.name == "hidden":
            btn.visible = False
        elif obj.name == "test21":
            btn.choices = [self.test21]

    @view(permission=["auth.view_user"])
    def test1(self: ExtraButtonsMixin, request: HttpRequest) -> None:
        self.message_user(request, "You have selected test1")

    @view()
    def test2(self: ExtraButtonsMixin, request: HttpRequest) -> None:
        self.message_user(request, "You have selected test2")

    @choice(change_list=False, change_form=True)
    def menu2(self, button: "ChoiceButton") -> None:
        button.choices = [self.test21, self.test22]

    @view()
    def test21(self: ExtraButtonsMixin, request: HttpRequest, pk: str) -> None:
        context = self.get_common_context(request, pk)
        self.message_user(request, f"You have selected test21 on {context['original']}")

    @view()
    def test22(self: ExtraButtonsMixin, request: HttpRequest, pk: str) -> TemplateResponse:
        context = self.get_common_context(request, pk)
        self.message_user(request, f"You have selected test22 on {context['original']}")
        return TemplateResponse(request, "demo/test22.html", context)

    @login_required
    @view()
    def test_login_required(self: ExtraButtonsMixin, request: HttpRequest, pk: str) -> TemplateResponse:
        context = self.get_common_context(request, pk)
        self.message_user(request, f"You have selected test22 on {context['original']}")
        return TemplateResponse(request, "demo/test22.html", context)

    def get_action_buttons(self: ExtraButtonsMixin, context: Any) -> "list[HandlerWithButton]":
        return [
            h
            for h in self.extra_button_handlers.values()
            if h.name
            in [
                "menu2",
            ]
        ]


admin.site.register(DemoModel1, Admin1)
admin.site.register(DemoModel2, Admin2)
admin.site.register(DemoModel3, Admin3)
admin.site.register(DemoModel4, Admin4)
admin.site.register(DemoModel5, Admin5)
