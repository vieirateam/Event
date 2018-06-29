"use strict"

let input = 0;
let preview = 0;
imgInput()

function imgInput() {
    input = document.querySelector('.image-input');
    preview = document.querySelector('.preview-image');
    input.style.opacity = 0;
    input.addEventListener('change', updateImageDisplay);
}

function updateImageDisplay() {
    let currentFiles = input.files;

    if(currentFiles.length !== 0) {
        if(validFileType(currentFiles[0])) {
            let reader  = new FileReader();

            reader.addEventListener("load", function () {
                preview.src = reader.result;
            }, false);
            
            reader.readAsDataURL(currentFiles[0]);
        } else {
            $("#error").text('Imagem ' + currentFiles[0].name + ' não contém um tipo válido.');
            $("#alert-display").show();
        }
    }
}


function validFileType(file) {
    let fileTypes = ['image/jpg','image/jpeg','image/png'];

    for(let i = 0; i < fileTypes.length; i++) {
        if(file.type === fileTypes[i]) {
            return true;
        }
    }

    return false;
}

function onClick(element) {
    $("#event-image").attr('src', element.src);
    $("#image-modal").show();
}