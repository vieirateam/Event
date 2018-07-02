"use strict"

$(function() {
    $('#vt_sidebar').hide();
    $('#vt_search_input').hide();

    $('#vt_nav_menu').click(function() {
        $('#vt_sidebar').show();
        $('#vt_overlay').show();
    });

    $('#vt_overlay').click(function() {
        $('#vt_sidebar').fadeOut();
        $('#vt_overlay').fadeOut();
    });

    $('#vt_search_button').click(function() {
        if($('#vt_search_input:hidden').length > 0) {
            let list;
            getJson($('#url_search'), function(response) {
                list = response;
            });

            $('#vt_search_input').fadeIn();
            $('#vt_search_input').focus();
            $('#vt_search_button').children().removeClass('fa-search');
            $('#vt_search_button').children().addClass('fa-remove');
            
            setTimeout(function() {
                $.each(list, function(i, item) {
                    let url_detail = $('#url_detail').attr('data-url').slice(0, -2);
                    let html = '<a href="'+url_detail+list[i].id+'" class="link-decoration">'+'<li>'+list[i].name+'</li></a>';
                    $('#vt_search_list').children('.w3-ul').append(html);
                });
            }, 500);
        } else {
            $('#vt_search_input').fadeOut();
            $('#vt_search_button').children().removeClass('fa-remove');
            $('#vt_search_button').children().addClass('fa-search');
        }
    });

    $('#vt_search_input').blur(function() {
        if($("#vt_search_list:hover").length <= 0) {
            $('#vt_search_input').fadeOut();
            $('#vt_search_button').children().removeClass('fa-remove');
            $('#vt_search_button').children().addClass('fa-search');
            $('#vt_search_list').fadeOut();
            $('#vt_search_list').children('.w3-ul').children('a').remove();
            $('#vt_search_input').val('');
        }
    });

    $('#vt_search_input').keyup(function() {
        if($(this).val().length > 2) {
            let text = $(this).val().toLowerCase();
            $('#vt_search_list').fadeIn();
            $('#vt_search_list ul li').filter(function() {
                $(this).toggle($(this).text().toLowerCase().indexOf(text) > -1);
            });
        } else {
            $('#vt_search_list').fadeOut();
        }
    });

    function getJson(id, success) {
        let url = id.attr('data-url');
        $.get(url, function(response) {
            success(response);
        });
    }

    $('#vt_dropdown_menu').click(function() {
        getJson($('#url'), function(response) {
            $('#vt_badge').text(response.number);
        });
        
        if($('#user_menu:hidden').length > 0) {
            $('#user_menu').fadeIn();
        } else {
            $('#user_menu').fadeOut();
        }
    });

    $('#vt_dropdown_menu').blur(function() {
        if($("#user_menu:hover").length <= 0) {
            $('#user_menu').fadeOut();
        }
    });
});