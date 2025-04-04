# How To

## Build two steps action

This example shows how to create a button that display a form to upload a file and process it.

**admin_extra_buttons/upload.html**

```html {% raw %}
{% extends "admin_extra_buttons/action_page.html" %}
{% load i18n static admin_list admin_urls %}

{% block action-content %}
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Upload</button>
</form>

{% endblock
{% endraw %}
```

**admin.py**

```python
from django import forms
from admin_extra_buttons.api import ExtraButtonsMixin, button
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import admin_urlname

class UploadForm(forms.Form):
    docfile = forms.FileField(label='Select a file')


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
                return redirect(admin_urlname(context['opts'], 'changelist'))
        else:
            form = UploadForm()
        context['form'] = form
        return TemplateResponse(request, 'admin_extra_buttons/upload.html', context)
```

## Customise @choice() options

When using [[@choice]] To render different options in the select widget just do this:


```python
from django.contrib import admin
from admin_extra_buttons.api import ExtraButtonsMixin, choice, view


class MyModelAdmin(ExtraButtonsMixin, admin.ModelAdmin):

    @choice(label="Menu #1", change_list=False, change_form=True)
    def menu1(self, button):
        original = button.original
        if original.field == "opt1":
            button.label = "Features for Case #1"
            button.choices = [self.feat1, ]
        elif original.field == "opt2":
            button.label = "Features for Case #2"
            button.choices = [self.feat2, ]
        else:
            button.visible = False

    @view()
    def feat1(self, request, pk):
        self.message_user(request, "You have selected Feature #1")

    @view()
    def feat2(self, request, pk):
        self.message_user(request, "You have selected Feature #2")


```
