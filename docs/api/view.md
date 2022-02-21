# @view()

Use this decorator to add views to any ModelAdmin. This decorator will not create any button.

## Options

pattern: `<function_name>/<path:arg1>/<path:arg2>/....`
: url pattern to use for the url generation. 

permission: `None`
:   Django permission code needed to access the view and display the button. Can be a callable

login_required: `True`
: Set to False to allow access to  anonymous users 

http_basic_auth: `False`
: Enable Basic Authentication for this view 

## Examples

### Simple

    @register(MyModel)
    class MyModelAdmin(ExtrButtonsMixi, admin.ModelAdmin):
        
        @view()
        def sele(self, request):

### HTTP Basic Authentication

    @register(MyModel)
    class MyModelAdmin(ExtrButtonsMixi, admin.ModelAdmin):

        @view(http_basic_auth=True)
        def api4(self, request):
            return HttpResponse("Basic Authentication allowed")
