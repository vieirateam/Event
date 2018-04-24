var myIndex = 0;
var slideIndex = 1;

carousel();
showDivs(slideIndex);

function carousel() {
    var i;
    var x = document.getElementsByClassName("mySlides");
    
    for (i = 0; i < x.length; i++) {
       x[i].style.display = "none";  
    }
    
    myIndex++;
    
    if (myIndex > x.length) {
    	myIndex = 1
    }

    x[myIndex-1].style.display = "block";
    slideIndex = myIndex;  
	showDivs(slideIndex);
    setTimeout(carousel, 4000); 
}

function plusDivs(n) {
	myIndex += n;
	showDivs(slideIndex += n);
}

function currentDiv(n) {
	myIndex = n;
	showDivs(slideIndex = n);
}

function showDivs(n) {
	var i;
	var x = document.getElementsByClassName("mySlides");
	var dots = document.getElementsByClassName("demo");
	
	if (n > x.length) {
		slideIndex = 1
	}    
	if (n < 1) {
		slideIndex = x.length
	}
	
	for (i = 0; i < x.length; i++) {
		x[i].style.display = "none";  
	}
	
	for (i = 0; i < dots.length; i++) {
		dots[i].className = dots[i].className.replace(" w3-white", "");
	}
	
	x[slideIndex-1].style.display = "block";  
	dots[slideIndex-1].className += " w3-white";
}

function showElement(element, elementClass) {
    if (element.className.indexOf(elementClass) == -1) {
        element.className += " " + elementClass;
    } else { 
        element.className = element.className.replace(" "+elementClass, "");
    }
}

function search(element) {
    showElement(element, "w3-show");
    div_list = document.getElementById('div-list');
    showElement(div_list, "w3-show");
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