import os

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse

from admin_extra_buttons.api import ExtraButtonsMixin, button, choice, confirm_action, link, view

from .models import DemoModel1, DemoModel2, DemoModel3, DemoModel4, DemoModel5
from .upload import UploadMixin


class TestFilter(SimpleListFilter):
    parameter_name = 'filter'
    title = "Dummy filter for testing"

    def lookups(self, request, model_admin):
        return (
            ('on', "On"),
            ('off', "Off"),
        )

    def queryset(self, request, queryset):
        return queryset


class Admin1(ExtraButtonsMixin, admin.ModelAdmin):
    list_filter = [TestFilter]

    @button(permission='demo.add_demomodel1',
            change_form=True,
            change_list=False,
            html_attrs={'class': 'aeb-green'})
    # html_attrs={'style': 'background-color:#88FF88;color:black'})
    def refresh(self, request):
        self.message_user(request, 'refresh called')

    @button(label='Refresh', permission=lambda request, object, **kw: False)
    def refresh_callable(self, request):
        opts = self.model._meta
        self.message_user(request, 'refresh called')
        return HttpResponseRedirect(reverse(admin_urlname(opts, 'changelist')))

    @button(pattern='a/b/')
    def custom_path(self, request):
        opts = self.model._meta
        self.message_user(request, "You invoked `custom_path` linked to 'a/b/' url ")
        return HttpResponseRedirect(reverse(admin_urlname(opts, 'changelist')))

    @button(html_attrs={'style': 'background-color:#EDD372;color:black'})
    def no_response(self, request):
        self.message_user(request, 'No Response provided.')

    @button(html_attrs={'style': 'background-color:#DC6C6C;color:black'})
    def confirm(self, request):
        def _action(request):
            pass

        return confirm_action(self, request, _action, "Confirm action",
                              "Successfully executed", )

    @button(permission='demo.delete_demomodel1')
    def update(self, request, pk):
        opts = self.model._meta
        self.message_user(request, 'action called')
        return HttpResponseRedirect(reverse(admin_urlname(opts, 'changelist')))

    @button()
    def no_response_single(self, request, object_id):
        self.message_user(request, 'No_response_obj.')

    @button(permission=lambda request, obj, **kw: False)
    def update_callable_permission(self, request, object_id):
        opts = self.model._meta
        self.message_user(request, 'action called')
        return HttpResponseRedirect(reverse(admin_urlname(opts, 'changelist')))

    @button(pattern='a/b/<path:object_id>')
    def custom_update(self, request, object_id):
        opts = self.model._meta
        self.message_user(request, 'action called')
        return HttpResponseRedirect(reverse(admin_urlname(opts, 'changelist')))

    @button(visible=lambda btn: 'BTN_SHOW' in os.environ)
    def custom_visibile(self, request):
        pass

    @button(enabled=False)
    def disabled(self, request):
        pass

    @button(enabled=lambda btn: 'BTN_ENABLED' in os.environ)
    def enabled(self, request):
        pass

    @link(href="https://www.google.com/", visible=lambda btn: True)
    def invisible(self, button):
        button.visible = False

    @button()
    def error_message(self, request):
        try:
            1 / 0
        except Exception as e:
            self.message_error_to_user(request, e)


class Admin2(ExtraButtonsMixin, admin.ModelAdmin):
    @link(href="https://www.google.com/", change_form=False, html_attrs={'target': '_new'})
    def google(self, button):
        pass

    @link(href=None, change_list=False, html_attrs={'target': '_new', 'style': 'background-color:var(--button-bg)'})
    def search_on_google(self, button):
        original = button.context['original']
        button.label = f"Search '{original.name}' on Google"
        button.href = f"https://www.google.com/?q={original.name}"

    @link(href="/", visible=lambda btn: 'BTN_SHOW2' in os.environ, change_list=True)
    def custom_visibile(self, button):
        pass


class Admin3(ExtraButtonsMixin, admin.ModelAdmin):
    @view()
    def api1(self, request):
        return HttpResponse("OK")

    @view()
    def api2(self, request, pk):
        return HttpResponse(pk)

    @view(login_required=False)
    def api3(self, request):
        return HttpResponse("Anonymous access allowed")

    @view(http_basic_auth=True)
    def api4(self, request):
        return HttpResponse("Basic Authentication allowed")


class Admin4(UploadMixin, admin.ModelAdmin):
    upload_handler = lambda *args: [1, 2, 3]  # noqa


class Admin5(ExtraButtonsMixin, admin.ModelAdmin):
    list_filter = [TestFilter]

    @choice(change_list=True, label="Menu #1")
    def menu1(self, button):
        button.choices = [self.test1, self.test2, self.test21]

    @view()
    def test1(self, request):
        self.message_user(request, "You have selected test1")

    @view()
    def test2(self, request):
        self.message_user(request, "You have selected test2")

    @choice(change_list=False, change_form=True)
    def menu2(self, button):
        button.choices = [self.test21, self.test22]

    @view()
    def test21(self, request, pk):
        context = self.get_common_context(request, pk)
        self.message_user(request, f"You have selected test21 on {context['original']}")

    @view()
    def test22(self, request, pk):
        context = self.get_common_context(request, pk)
        self.message_user(request, f"You have selected test22 on {context['original']}")
        return TemplateResponse(request, "demo/test22.html", context)

    def get_action_buttons(self, context):
        return [h for h in self.extra_button_handlers.values() if h.name in ['menu2', ]]


admin.site.register(DemoModel1, Admin1)
admin.site.register(DemoModel2, Admin2)
admin.site.register(DemoModel3, Admin3)
admin.site.register(DemoModel4, Admin4)
admin.site.register(DemoModel5, Admin5)
