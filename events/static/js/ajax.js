"use strict"

$(function() {
    let url = $('#url').attr('data-url');
    $.get(url, function(response) {
        $('#vt_badge').text(response.number);
    });
});