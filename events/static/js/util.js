"use strict"

function display(element, value) {
    $('#'+element).css('display',value);
}

function dateTimeFunction(initialElementId, lastElementId) {
    let minValue = $('#'+initialElementId).val();
    $('#'+lastElementId).attr('min', minValue);
}

function dateRange(elementEventId,elementDateId) {
    let eventOption = $('#'+elementEventId+' option:selected').val();
    let value = eventsList[eventOption-1][0];
    $('#'+elementDateId).attr('min', value);
    value = eventsList[eventOption-1][1];
    $('#'+elementDateId).attr('max', value);
}

function timeFunction(elementDateId, elementTimeId) {
    let inputDate = $('#'+elementDateId).val();
    let date = new Date();

    let day = checkDateTime(date.getDate());
    let month = checkDateTime(date.getMonth() + 1);
    let hours = checkDateTime(date.getHours());
    let minutes = checkDateTime(date.getMinutes());

    let currentDate = date.getFullYear() + "-" + month + "-" + day;
    
    if(inputDate == currentDate) {
        let time = hours + ":" + minutes;
        $('#'+elementTimeId).attr('min', time);
    } else {
        $('#'+elementTimeId).attr('min', "");
    }
}

function checkDateTime(dateTime) {
    if(dateTime < 10) {
        return "0" + dateTime;
    }
    return dateTime;
}

function selectSpeaker() {
    if($("#speaker_id")[0] != null) {
        $("#speaker_id").attr('selected', "selected");
    }
}