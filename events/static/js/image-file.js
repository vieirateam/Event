var input = 0;
var preview = 0;
imgInput()

function imgInput() {
    input = document.querySelector('.image-input');
    preview = document.querySelector('.preview-image');
    input.style.opacity = 0;
    input.addEventListener('change', updateImageDisplay);
}

function updateImageDisplay() {
    var currentFiles = input.files;

    if(currentFiles.length !== 0) {
        if(validFileType(currentFiles[0])) {
            var reader  = new FileReader();

            reader.addEventListener("load", function () {
                preview.src = reader.result;
            }, false);
            
            reader.readAsDataURL(currentFiles[0]);
        } else {
            document.getElementById("error").innerHTML = 'Imagem ' + currentFiles[0].name + ' não contém um tipo válido.';
            document.getElementById("alert-display").style.display = "block";
        }
    }
}


function validFileType(file) {
    var fileTypes = ['image/jpg','image/jpeg','image/png'];

    for(var i = 0; i < fileTypes.length; i++) {
        if(file.type === fileTypes[i]) {
            return true;
        }
    }

    return false;
}

function onClick(element) {
    document.getElementById("event-image").src = element.src;
    document.getElementById("image-modal").style.display = "block";
}