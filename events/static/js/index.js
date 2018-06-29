"use strict"

let myIndex = 0;
let slideIndex = 1;

carousel();
showDivs(slideIndex);

function carousel() {
    let i;
    let x = $(".mySlides");
    
    x.each(function(index) {
        $(this).hide();
    });
    
    myIndex++;
    
    if (myIndex > x.length) {
        myIndex = 1
    }

    $(".mySlides:eq("+myIndex+")").show();
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
    let i;
    let x = $(".mySlides");
    let dots = $(".demo");
    
    if (n > x.length) {
        slideIndex = 1
    }    
    if (n < 1) {
        slideIndex = x.length
    }
    slideIndex -= 1;
    
    x.each(function(index) {
        $(this).hide();
    });
    
    dots.each(function(index) {
        $(this).removeClass("w3-white");
    })
    
    $(".mySlides:eq("+slideIndex+")").show();  
    $(".demo:eq("+slideIndex+")").addClass("w3-white");
}