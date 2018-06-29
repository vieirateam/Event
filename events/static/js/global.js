"use strict"

function showElement(elementId, elementClass) {
    $('#'+elementId).toggleClass(elementClass);
}

function search(elementId) {
    showElement(elementId, "w3-show");
    showElement("div-list", "w3-show");
    $('#'+elementId).focus();
    let searchButton = $('#search-button')[0];
    let iconReplace = "";
    let iconRemove = "";
    if (searchButton.className.indexOf("fa-search") == -1) {
        iconRemove = " fa-remove";
        iconReplace = " fa-search";
    } else {
        iconRemove = " fa-search";
        iconReplace = " fa-remove";
    }
    $('#search-button').removeClass(iconRemove);
    $('#search-button').addClass(iconReplace);
}

function filterElement() {
    let input, filter, list, listItems, i;
    input = $("#search-bar")[0];
    filter = input.value.toUpperCase();
    $("#list").children().each(function(index) {
        if($(this)) {
            if($(this).text().toUpperCase().indexOf(filter) > -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        }
    })
}