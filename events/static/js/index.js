"use strict"

let slideIndex = 1;
showDivs(slideIndex);

function plusDivs(index) {
    showDivs(slideIndex += index);
}

function showDivs(index) {
    let i;
    let x = document.getElementsByClassName("show-slides");
    if (index > x.length) {
        slideIndex = 1
    }
    if (index < 1) {
        slideIndex = x.length
    };
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    x[slideIndex-1].style.display = "block";
}