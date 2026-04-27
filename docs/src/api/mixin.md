# ExtraButtonMixin

Mixin to use with ModelAdmin to properly handle button [decorators]()

## Attributes

change_list_template
: Default `admin_extra_buttons/change_list.html`


change_form_template
: Default `admin_extra_buttons/change_form.html`


extra_button_handlers
: Dictionary of button/link/choice handlers indexed by handler name.
Populated during `get_extra_urls()`.


## Methods

get_extra_urls()
: Returns a list of URL patterns for `@view` decorated methods.
This method scans the class MRO for BaseExtraHandler instances,
creates unique URL names, applies decorators in reverse order,
and returns URL patterns.

get_urls()
: Returns the combined list of extra URLs and Django admin URLs.
Calls `get_extra_urls()` and extends with `admin.ModelAdmin.get_urls()`.


get_changeform_buttons(context)
: Return the list of buttons that will be displayed on the change form page.
Default implementation returns all the buttons with `change_form=True` or `change_form=None`

get_changelist_buttons(context)
: Return the list of buttons that will be displayed on the changelist page.
Default implementation returns all the buttons with `change_list=True` or `change_list=None`


get_action_buttons(context)
: Return the list of buttons that will be displayed on the extra action page.
Default implementation returns an empty list.


get_common_context()
: This method returns a django template Context filled with the common values
that can be useful when create custom views that render templates. (\@see [Build two steps action](../howto.md#build-two-steps-action))

message_error_to_user()
: Shortcut to display message on Exception

media
: Returns the combined media including Django admin media and extra_buttons CSS/JS.


check(\**kwargs)
: Extends Django admin check() to validate decorators.
Calls parent check() and adds decorator validation errors.
