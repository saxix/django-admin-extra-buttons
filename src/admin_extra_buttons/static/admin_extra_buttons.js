(function ($) {
    $("li a.aeb-disable-on-click").click(function (e) {
        if ($(this).hasClass("disabled")) {
            e.preventDefault();
        } else {
            $(this).removeClass("btn-success").addClass("disabled");
        }
    });

    var update = function (frm) {
        return function () {
            var changes = frm.serialize();
            if (changes !== frm.data("serialized")) {
                $(".object-tools").find("a.aeb-disable_on_edit").not('.disabled').addClass("disabled").addClass("auto");
            } else {
                $(".object-tools").find("a.aeb-disable_on_edit.disabled.auto").removeClass("disabled").removeClass("auto");
            }
        };
    };
    $(function () {
        $("FORM").each(function (i, form) {
            var $form =$(form);
            $form.data("serialized", $form.serialize());
            $form.on("change input", update($form));
        });
    });
})
(django.jQuery);
