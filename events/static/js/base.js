"use strict"

$(function() {
    function getJson() {
        let url = $('#url').attr('data-url');
        $.get(url, function(response) {
            $('#vt_badge').text(response.number);
        });
    }

    $('#vt_dropdown_menu').click(function() {
        getJson();
        if($('#user_menu:hidden').length > 0) {
            $('#user_menu').show();
        } else {
            $('#user_menu').hide();
        }
    });

    $('#vt_dropdown_menu').blur(
        function() {
            if($("#user_menu:hover").length <= 0) {
                $('#user_menu').hide();
            }
        }
    );
});