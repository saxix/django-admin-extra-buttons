from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from admin_extra_buttons.api import ExtraButtonsMixin, button, confirm_action, link, view

from .models import DemoModel1, DemoModel2, DemoModel3, DemoModel4
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

    @button(permission='demo.add_demomodel1', html_attrs={'style': 'background-color:#88FF88;color:black'})
    def refresh(self, request):
        opts = self.model._meta
        self.message_user(request, 'refresh called')
        return HttpResponseRedirect(reverse(admin_urlname(opts, 'changelist')))

    @button(label='Refresh', permission=lambda request, object: False)
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

    @button(permission=lambda request, obj: False)
    def update_callable_permission(self, request, object_id):
        opts = self.model._meta
        self.message_user(request, 'action called')
        return HttpResponseRedirect(reverse(admin_urlname(opts, 'changelist')))

    @button(pattern='a/b/<path:object_id>')
    def custom_update(self, request, object_id):
        opts = self.model._meta
        self.message_user(request, 'action called')
        return HttpResponseRedirect(reverse(admin_urlname(opts, 'changelist')))

    @button()
    def wizard(self, request, object_id):
        return Tem(reverse(admin_urlname(opts, 'changelist')))


class Admin2(ExtraButtonsMixin, admin.ModelAdmin):
    @link(href="https://www.google.com/", change_form=False, html_attrs={'target': '_new'})
    def google(self, button):
        pass

    @link(href=None, change_list=False, html_attrs={'target': '_new', 'style': 'background-color:var(--default-button-bg)'})
    def search_on_google(self, button):
        original = button.context['original']
        button.label = f"Search '{original.name}' on Google"
        button.href = f"https://www.google.com/?q={original.name}"


class Admin3(ExtraButtonsMixin, admin.ModelAdmin):
    @view()
    def api1(self, request):
        return HttpResponse("OK")

    @view()
    def api2(self, request, pk):
        return HttpResponse(pk)


class Admin4(UploadMixin, admin.ModelAdmin):
    upload_handler = lambda *args: [1, 2, 3]  # noqa


admin.site.register(DemoModel1, Admin1)
admin.site.register(DemoModel2, Admin2)
admin.site.register(DemoModel3, Admin3)
admin.site.register(DemoModel4, Admin4)
