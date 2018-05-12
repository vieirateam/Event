function display(element, value) {
    document.getElementById(element).style.display=value;
}

function dateTimeFunction(initialElementId, lastElementId) {
    var minValue = document.getElementById(initialElementId).value;
    document.getElementById(lastElementId).min = minValue;
}

function dateRange(elementEventId,elementDateId) {
    inputDate = document.getElementById(elementDateId);
    eventOption = document.getElementById(elementEventId);
    inputDate.min = eventsList[eventOption.selectedIndex-1][0];
    inputDate.max = eventsList[eventOption.selectedIndex-1][1];
}

function timeFunction(elementDateId, elementTimeId) {
    inputDate = document.getElementById(elementDateId).value;
    var date = new Date();

    day = checkDateTime(date.getDate());
    month = checkDateTime(date.getMonth() + 1);
    hours = checkDateTime(date.getHours());
    minutes = checkDateTime(date.getMinutes());

    var currentDate = date.getFullYear() + "-" + month + "-" + day;
    
    if(inputDate == currentDate) {
        var time = hours + ":" + minutes;
        document.getElementById(elementTimeId).min = time;
    } else {
        document.getElementById(elementTimeId).min = "";
    }
}

function checkDateTime(dateTime) {
    if(dateTime < 10) {
        return "0" + dateTime;
    }
    return dateTime;
}

function selectSpeaker() {
    if(document.getElementById("speaker_id") != null) {
        document.getElementById("speaker_id").selected = "selected";
    }
}