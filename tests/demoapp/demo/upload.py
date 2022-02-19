from django.contrib import messages
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse

from admin_extra_buttons.api import ExtraButtonsMixin, button


class UploadMixin(ExtraButtonsMixin):
    upload_handler = None
    upload_form_template = 'admin_extra_buttons/upload.html'

    def get_upload_form_template(self, request):
        return self.upload_form_template

    @button(icon='icon-upload')
    def upload(self, request):
        context = self.get_common_context(request, title='Upload', help_text=self.upload_handler.__doc__, )

        if request.method == 'POST':
            if 'file' in request.FILES:
                try:
                    f = request.FILES['file']
                    rows, updated, created = self.upload_handler(f)
                    msg = "Loaded {}. Parsed:{} " \
                          "updated:{} created:{}".format(f.name,
                                                         rows,
                                                         updated,
                                                         created)
                    self.message_user(request, msg, messages.SUCCESS)
                    return HttpResponseRedirect(reverse(admin_urlname(self.model._meta,
                                                                      'changelist')))
                except Exception as e:
                    self.message_user(request, str(e), messages.ERROR)

        return TemplateResponse(request,
                                self.get_upload_form_template(request),
                                context)
