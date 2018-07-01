"use strict"

$(function() {
    $('#vt_approve').click(function() {
        let url = $('#url_approve').attr('data-url');
        
        $.get(url, function(response) {
            console.log(response);
            if (response.status) {
                $('#vt_approve').remove();
                $('#vt_remove').remove();
                $('#vt_remove_dialog').remove();
            }
        });
    });

    $('#vt_remove').click(function() {
        $('#vt_remove_dialog').show();
    });

    $('.vt_hide_dialog').click(function() {
        $('#vt_remove_dialog').hide();
    })
});