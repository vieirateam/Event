"use strict"

$(function() {
    getJson();

    function getJson() {
        let url = $('#url').attr('data-url');
        $.get(url, function(response) {
            $('#vt_badge').text(response.number);
        });
    }

    if($('#url_talk') != null && $('#url_speaker') != null) {
        $('#vt_talk_approve').click(function() {
            let url_talk = $('#url_talk').attr('data-url');
            $.get(url_talk, function(response) {
                console.log(response);
            });
            getJson();
            $(this).parent().hide();
        });
        $('#vt_speaker_approve').click(function() {
            let url_speaker = $('#url_speaker').attr('data-url');
            $.get(url_speaker, function(response) {
                console.log(response);
            });
            getJson();
            $(this).parent().hide();
        });
    }
});