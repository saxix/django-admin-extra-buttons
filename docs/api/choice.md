# @choice()

This decorator allows "grouping" different `@view()` decorated methods under the same HTML `<select>` 


Examples:
    
    from admin_extra_buttons.api import ExtraButtonsMixin, choice, view

    class MyModelAdmin(ExtraButtonsMixin, admin.ModelAdmin):
        @choice(change_list=True)
        def menu1(self, button):
            button.choices = [self.test1, self.test2]
    
        @view()
        def test1(self, request):
            self.message_user(request, "You have selected test1")
    
        @view()
        def test2(self, request, pk):
            context = self.get_common_context(request, pk)
            self.message_user(request, f"You have selected test22 on {context['original']}")
            return TemplateResponse(request, "demo/test22.html", context)
     

## Options

change_form: `True`
: display the button on the `change_form` page

change_list: `True`
: display  the button on the `change_list` page

enabled: `True`
: bool or callable to set enable status

html_attrs: `{}`
: Dictionary of html tags to use in button rendering

label: `decorated method name`
: button label

visible: `True`
: bool or callable show/hide button


### Attributes

context
: TemplateContext from the Django template as at the moment of rendering

## Examples

### Complex Configuration

    class MyModelAdmin(ExtraButtonsMixin, admin.ModelAdmin):

        @choice(label="Menu #1",
                change_list=False,
                html_attrs={'target': '_new', 'style': 'background-color:var(--button-bg)'})
        def menu1(self, button):
            original = button.original
            button.label = f"Search '{original.name}' on Google"
            if button.requst.user.is_superuser: 
                button.choices = [self.feat1, self.feat2, self.feat3, self.feat4]
            else:
                button.choices = [self.feat1, self.feat2]

        @view()
        def feat1(self, request):
            self.message_user(request, "You have selected Feature #1") 

        @view()
        def feat2(self, request):
            return TemplateResponse(request, "demo/feat2.html", context)

        @view(permission=lambda request, obj: request.user.is_superuser)
        def feat3(self, request):
            return HttpResponse("You have selected Feature #3") 

        @view(permission=lambda request, obj: request.user.is_superuser)
        def feat3(self, request):
            self.message_user(request, "You have selected Feature #3") 
