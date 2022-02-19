# ExtraButtonMixin

This Mixin n 

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
: This method returns a standard django template Context that can be useful when create custom views 

message_error_to_user()
: Shortcut to display message on Exception

