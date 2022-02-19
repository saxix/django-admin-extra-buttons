@button
-------

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


    MkDocs [community wiki]. If you want to share a theme you create, you
    should list it on the Wiki.

