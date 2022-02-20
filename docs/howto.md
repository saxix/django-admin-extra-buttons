# How To

## Build two steps action

This example shows how to create a button that display a form to upload a file and process it.

`admin_extra_buttons/upload.html`

    {% extends "admin_extra_buttons/action_page.html" %}
    {% load i18n static admin_list admin_urls %}
    
    {% block action-content %}
      <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Upload</button>
      </form>
    
    {% endblock %}

`admin.py`

    class UploadForm(forms.Form):
        docfile = forms.FileField( label='Select a file')

    class MyModelAdmin(ExtraButtonsMixin, admin.ModelAdmin):

        @button()
        def upload(self, request):
            context = self.get_common_context(request, title='Upload')
            if request.method == 'POST':
                form = UploadForm(request.POST, request.FILES)
                if form.is_valid():
                    downloaded_file = request.FILES['docfile']
                    # process file
                    ...
                    ...
                    return redirect(admin_urlname(context['opts'], 'changelist') )
            else:
                form = UploadForm()
            context['form'] = form
            return TemplateResponse(request, 'admin_extra_buttons/upload.html', context)

