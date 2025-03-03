# Handlers

!!! Warning

    This is an internal API and should be used only for extend/customise core behaviours.

``` mermaid
classDiagram
    BaseExtraHandler <-- ViewHandler
    ButtonMixin <-- ButtonHandler
    ViewHandler <-- ButtonHandler

    ButtonMixin <-- LinkHandler
    BaseExtraHandler <-- LinkHandler

    LinkHandler <-- ChoiceHandler

    Button <-- LinkButton
    LinkButton <-- ChoiceButton

```

[//]: # (## ButtonHandler)

[//]: # (View handler for `@button` decorated views)



::: admin_extra_buttons.handlers.BaseExtraHandler

::: admin_extra_buttons.handlers.ViewHandler

::: admin_extra_buttons.handlers.ButtonHandler

::: admin_extra_buttons.handlers.LinkHandler

::: admin_extra_buttons.handlers.ChoiceHandler

::: admin_extra_buttons.handlers.ButtonMixin

::: admin_extra_buttons.buttons.LinkButton

::: admin_extra_buttons.buttons.ChoiceButton


[//]: # ()
[//]: # (View handler for `@view` decorated views)

[//]: # ()
[//]: # (::: admin_extra_buttons.handlers.ButtonHandler)

[//]: # ()
[//]: # ()
[//]: # ()
[//]: # (::: admin_extra_buttons.handlers.LinkHandler)

[//]: # ()
[//]: # (View handler for `@link` decorated views)

[//]: # ()
[//]: # ()
[//]: # (## ViewButton)

[//]: # ()
[//]: # (Button class for Django views based buttons )

[//]: # ()
[//]: # ()
[//]: # (## LinkButton)

[//]: # ()
[//]: # (Button class for links based buttons &#40;buttons not linked to Django views&#41;  )

[//]: # ()
[//]: # ()
[//]: # (## ChoiceButton)

[//]: # ()
[//]: # (Button class for choices buttons  )
