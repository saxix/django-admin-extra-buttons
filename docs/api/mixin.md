# ExtraButtonMixin

Mixin to use with ModelAdmin to properly handle button [decorators]()

## Attributes

change_list_template
: Default `admin_extra_buttons/change_list.html`


change_form_template
: Default `admin_extra_buttons/change_form.html`

## Methods

get_changeform_buttons(context)
: Return the list of buttons that will be displayed on the change form page.
Default implementation returns all the buttons with `change_form=True` or `change_form=None`

get_changelist_buttons(context)
: Return the list of buttons that will be displayed on the changelist page.
Default implementation returns all the buttons with `change_list=True` or `change_list=None`


get_action_buttons(context)
: Return the list of buttons that will be displayed on the extra action page.

get_common_context()
: This method returns a django template Context filled with the common values 
that can be useful when create custom views that render templates. (\@see [Build two steps action](/howto/#build-two-steps-action))

message_error_to_user()
: Shortcut to display message on Exception

