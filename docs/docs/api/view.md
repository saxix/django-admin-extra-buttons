# @view()

Use this decorator to add views to any ModelAdmin. This decorator will not create any button.

## Options

pattern:
: url pattern to use for the url genaration. Default to `<function_name>/<path:arg1>/<path:arg2>/....`

permission
:   Django permission code needed to access the view and display the button. Can be a callable

login_required
: Set to False to allow access to  anonymous users 

http_basic_auth
: Enable Basic Authentication for this url 

## Examples

### Simple
    @register(MyModel)
    class MyModelAdmin(ExtrButtonsMixi, admin.ModelAdmin):
        
        @view()
        def sele(self, request):
            
