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

---

!!! Note

    AEB try to understand if a button should appear in the `change_form` and/or in the `change_list` page.
    If the decorated method has only one argument (es. `def scan(self, request)`), the button will only be visible
    on the `change_list` page, if it contains more that one argumente (es. `def scan(self, request, pk)`)
    the button will be visible in the `change_form` page.

## Options

change_form: `None`
: set to `True` do show the button on the `change_form` page
  If set to `None` (default), use method signature to display the button 

change_list: `None`
: set to `True` do show the button on the `change_list` page
    If set to `None` (default), use method signature to display the button

disable_on_click: `True`
: automatically disable button on click() to prevent unintentional double processing

disable_on_edit: `True`
: automatically disable button when any FORM in page is modified

enabled: `True`
: bool or callable to set enable status

html_attrs: `{}`
: Dictionary of html tags to use in button rendering.

label: `decorated method name`
: button label

visible: `True`
: bool or callable show/hide button

   
!!! Note

    `id` is automacally set if not provided, 
    `class` is updated/set based on `disable_on_click` and `disable_on_edit` values 

label: `decorated method name`
: button label

pattern: `<function_name>/<path:arg1>/<path:arg2>/....`
: url pattern to use for the url genaration.
        
permission: `None`
:   Django permission code needed to access the view and display the button

## Examples

### Simple
Simplest usage. Display a button and create a view on `admin/mymodel/scan`.
    
    @register(MyModel)
    class MyModelAdmin(ExtrButtonsMixi, admin.ModelAdmin):
        
        @button()
        def scan(self, request):
            pass

### Check Permissions
Buttons with custom permission, one for `change_list` and other for `change_form`

    @register(MyModel)
    class MyModelAdmin(ExtrButtonsMixi, admin.ModelAdmin):
        
        @button(permission=lambda request, obj: request.user.is_superuser)
        def delete_all(self, request):
            pass

        @button(permission='app.delete_mymodel)
        def mark(self, request, pk):
            obj = self.get_object(request.pk)
            obj.mark = True
            obj.save()


### Fully featured
Buttons with custom permission, one for `change_list` and other for `change_form`

    @register(MyModel)
    class MyModelAdmin(ExtrButtonsMixi, admin.ModelAdmin):
        
        @button(permission=lambda request, obj: request.user.is_superuser,
                html_attrs={'style': 'background-color:var(--button-bg)'},
                label=_('Delete All Records'),
                change_form=True
                )
        def delete_all(self, request):
            pass

        @button(permission=lambda request, obj: request.user.is_superuser,
                html_attrs={'style': 'background-color:var(--button-bg)'},
                enabled=lambda btn: btn.original.status == SUCCESS,
                label=_('Delete All Records'),
                change_form=True
                )
        def toggle(self, request, pk):
            pass



