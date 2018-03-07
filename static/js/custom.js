$(document).ready(function () {
    "use strict";
    
    var valida = $(".box-form .form-control");
    valida.blur(function () {
        if ($(this).val() === '') {
            $(this).parent().find('.custom-alert').fadeIn(200)
        }
        else {
            $(this).parent().find('.custom-alert').fadeOut(100)
        }
    });
    $('.selectpicker').selectpicker();
    $('input.material-checkbox').on('change', function() {
        $(".hidde").slideUp(200);
        $(".material-checkbox:checked").each(function(){
            //alert($(this).attr('data-target'));
            $("."+$(this).attr('data-target')).slideDown(200);
        });

    });
});
