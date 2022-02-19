# @button()

This decorator transform any ModelAdmin method to a view and add a button to the Admin objects toolbar.

Examples:

    from admin_extra_buttons.api import ExtraButtonsMixin, button, confirm_action, link, view

    class MyModelAdmin(ExtraButtonsMixin, admin.ModelAdmin):
        @button()    
        def refresh_all(self, request):
            ...
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

---

!!! Note

    AEB try to understand if a button should appear in the `change_form` and/or in the `change_list` page.
    If the decorated method has only one argument (es. `def scan(self, request)`), the button will only be visible
    on the `change_list` page, if it contains more that one argumente (es. `def scan(self, request, pk)`)
    the button will be visible in the `change_form` page.

## Options

change_form
: set to `True` do show the button on the `change_form` page

change_list
: set to `True` do show the button on the `change_list` page

html_attrs
:   Dictionary of html tags to use in button rendering

pattern:
: url pattern to use for the url genaration.
    Default to `<function_name>/<path:arg1>/<path:arg2>/....`
        
permission
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
                change_
                )
        def delete_all(self, request):
            pass




