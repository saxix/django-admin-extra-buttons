# @button()

This decorator transform any ModelAdmin method to a view and add a button to the Admin objects toolbar.

Examples:

```python

from admin_extra_buttons.api import ExtraButtonsMixin, button


class MyModelAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    @button()
    def refresh_all(self, request):
        # your business logic here
        ...
        self.message_user(request, 'refresh called')
        # do not return HttpResponse(), so user will be redirected to the original page

    @button()
    def scan(self, request):
        return HttpResponse("Done")  # return specific response

    @button()
    def scan(self, request):
        if request.method == 'POST':
            ....
        else:
            return TemplateResponse()

```


!!! Note

    AEB can guess if the button should appear in the `change_form` and/or in the `change_list` page:
    if the decorated method has only one argument (es. `def scan(self, request)`), the button will only be visible
    on the `change_list` page ; while if it contains more that one argument (es. `def scan(self, request, pk)`)
    the button will be visible in the `change_form` page.

## Options

`change_form` (defaults to `None`):
    Set to `True` do show the button on the `change_form` page.
    If set to `None` (default), use method signature to display the button.

`change_list` (defaults to `None`):
    Set to `True` do show the button on the `change_list` page.
    If set to `None` (default), use method signature to display the button.

`disable_on_click` (defaults to `True`):
    Automatically disable button on `click` to prevent unintentional double processing.

`disable_on_edit` (defaults to `True`):
    Automatically disable button when any FORM in page is modified.

`enabled` (defaults to `True`):
    bool or callable to set enable status. The callable takes the `StandardButton` instance as a unique argument ; this argument gives access to the `request`, the template `context`, and the `original` object the is being edited in the admin.

`html_attrs` (defaults to `{}`):
    Dictionary of html tags to use in button rendering.

`label` (defaults to `decorated method name`):
    button label.

`pattern` (defaults to `<function_name>/<path:arg1>/<path:arg2>/....`):
    url pattern to use for the url generation.

`visible` (defaults to `True`):
    bool or callable show/hide button. The callable takes the `StandardButton` instance as a unique argument ; this argument gives access to the `request`, the template `context`, and the `original` object the is being edited in the admin.

`permission` (defaults to `None`):
    Django permission code needed to access the view and display the button, or a callable that takes the `request`, edited `object`, and `handler` as arguments and that must return a `bool`.

!!! Note

    `id` is automacally set if not provided,
    `class` is updated/set based on `disable_on_click` and `disable_on_edit` values

## Examples

### Simple

Simplest usage. Display a button and create a view on `admin/mymodel/scan`.

```python

@register(MyModel)
class MyModelAdmin(ExtrButtonsMixi, admin.ModelAdmin):

    @button()
    def scan(self, request):
        pass

```
### Check Permissions

Buttons with custom permission, one for `change_list` and other for `change_form`

```python

@register(MyModel)
class MyModelAdmin(ExtraButtonsMixin, admin.ModelAdmin):

    @button(permission=lambda request, obj, handler: request.user.is_superuser)
    def delete_all(self, request):
        pass

    @button(permission='app.delete_mymodel)
    def mark(self, request, pk):
        obj = self.get_object(request, pk)
        obj.mark = True
        obj.save()

```

### Fully featured

Two complex buttons, one for `change_list` with custom permission, and one for `change_form` with custom visibility.

```python

@register(MyModel)
class MyModelAdmin(ExtraButtonsMixin, admin.ModelAdmin):

    @button(permission=lambda request, obj, handler: request.user.is_superuser,
            html_attrs={'style': 'background-color:var(--button-bg)'},
            label=_('Delete All Records'),
            )
    def delete_all(self, request):
        pass

    @button(visible=lambda btn: "special_context_key" in btn.context,
            html_attrs={'style': 'background-color:var(--button-bg)'},
            enabled=lambda btn: btn.original.status == SUCCESS,
            label=_('Do something special on this one'),
            )
    def toggle(self, request, pk):
        pass

```
