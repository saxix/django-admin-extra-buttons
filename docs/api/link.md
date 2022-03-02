# @link()

Use this decorator if you want to create links to external 
resources or if you already have the required view. 


!!!Note
    
    @link() buttons by defaults are visible both on `change_list` and `change_form` pages


Examples:
    
    from admin_extra_buttons.api import ExtraButtonsMixin, link

    class MyModelAdmin(ExtraButtonsMixin, admin.ModelAdmin):
        @link(href="https://www.google.com/", change_form=False)
        def google(self, button):
            pass
    
        @link(href=None, change_list=False)
        def search_on_google(self, button):
            button.label = f"Search '{button.original.name}' on Google"
            button.href = f"https://www.google.com/?q={button.original.name}"
     

## Options

change_form: `True`
: display the button on the `change_form` page

change_list: `True`
: display  the button on the `change_list` page

href: `"""`
: HTML `href` attribute value 

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

### Dynamic Configuration

    class MyModelAdmin(ExtraButtonsMixin, admin.ModelAdmin):

        @link(href=None, change_list=False)
        def search_on_google(self, button):
            button.label = f"Search '{button.original.name}' on Google"
            button.href = f"https://www.google.com/?q={original.name}"

### Fully featured

    class MyModelAdmin(ExtraButtonsMixin, admin.ModelAdmin):

    @link(href=None, 
          change_list=False, 
          html_attrs={'target': '_new', 'style': 'background-color:var(--button-bg)'})
    def search_on_google(self, button):
        button.label = f"Search '{button.original.name}' on Google"
        button.href = f"https://www.google.com/?q={button.original.name}"
