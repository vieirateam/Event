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