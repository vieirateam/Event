function showElement(elementId, elementClass) {
    element = document.getElementById(elementId);
    if (element.className.indexOf(elementClass) == -1) {
        element.className += " " + elementClass;
    } else { 
        element.className = element.className.replace(" "+elementClass, "");
    }
}

function search(elementId) {
    showElement(elementId, "w3-show");
    showElement("div-list", "w3-show");
    element = document.getElementById(elementId);
    element.focus();
    searchButton = document.getElementById('search-button');
    iconReplace = "";
    iconRemove = "";
    if (searchButton.className.indexOf("fa-search") == -1) {
        iconRemove = " fa-remove";
        iconReplace = " fa-search";
    } else {
        iconRemove = " fa-search";
        iconReplace = " fa-remove";
    }
    searchButton.className = searchButton.className.replace(iconRemove, iconReplace);
}

function filterElement() {
    var input, filter, list, listItems, i;
    input = document.getElementById("search-bar");
    filter = input.value.toUpperCase();
    list = document.getElementById("list");
    listItems = list.getElementsByTagName("li");
    for(i = 0; i < listItems.length; i++) {
        if(listItems[i]) {
            if(listItems[i].innerHTML.toUpperCase().indexOf(filter) > -1) {
                listItems[i].style.display = "";
            } else {
                listItems[i].style.display = "none";
            }
        }
    }
}