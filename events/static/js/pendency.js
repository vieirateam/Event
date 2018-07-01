"use strict"

$(function() {
    $('.vt_approve').click(function() {
        let url = $(this).parent().children('.url').attr('data-url');
        $.get(url, function(response) {
            console.log(response);
            checkList($(this).parent().parent());
        });
    });

    $('.vt_close').click(function() {
        $(this).parent().hide();

        checkList($(this).parent().parent());
    });

    function checkList(id) {
        if(isHidden(id)) {
            id.append('<li class="w3-bar"><p>Não há pendências</p></li>');
        }
    }

    function isHidden(id) {
        return id.children(':hidden').length == $(id).children().length;
    }
});