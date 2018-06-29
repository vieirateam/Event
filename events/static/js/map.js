"use strict"

let map;
let marker;
let infowindow;

function initMap() {
    let inputLat = $("#id_latitude").val();
    let inputLng = $("#id_longitude").val();
    let page = $("#id_page").val();

    let initialZoom = 7;
    let finalZoom = 13;
    let content = "<h6 class='w3-center'>Canoinhas</h6>";

    if(page == "detail" || page == "Editar") {
        initialZoom = 16;
        finalZoom = 16;

        if(page == "Editar") {
            let title = $('#id_name').val();
            content = "<h6 class='w3-center'>" + title + "</h6>";
        } else {
            let title = $('#id_name').text();
            let date = $('#id_event_date').text();
            content = "<h6 class='w3-center'>" + title + "</h6>" + "<p class='w3-center w3-opacity'>" + date + "</p>";
        }
    }

    let mapCenter = new google.maps.LatLng(inputLat,inputLng);
    setMap(mapCenter, initialZoom);

    if(page == "Editar" || page == "new") {
        google.maps.event.addListener(map, 'click', function(event) {
            placeMarker(event.latLng);
        });
    }

    setMarker(mapCenter);
    setInfoWindow(content);
    setInfoWindowListenter();
    openInfoWindow();
}

function placeMarker(location) {
    mapZoom(location,16);
    marker.setMap(null);
    setMarker(location);

    let content = '<h7>Latitude: ' + location.lat() + '</h7><br><h7>Longitude: ' + location.lng() + '</h7>';
    setInfoWindow(content);
    openInfoWindow();

    setInfoWindowListenter();

    $("#id_latitude").val(location.lat());
    $("#id_longitude").val(location.lng());
}

function setMap(location, zoom) {
    let mapCanvas = $("#map")[0];
    let mapOptions = {center: location, zoom: zoom};
    map = new google.maps.Map(mapCanvas, mapOptions);
}

function setMarker(location) {
    marker = new google.maps.Marker({
        position: location,
        map: map
    });
}

function setInfoWindow(content) {
    infowindow = new google.maps.InfoWindow({
        content: content
    });
}

function setInfoWindowListenter() {
    google.maps.event.addListener(marker,'click',function() {
        openInfoWindow();
    });
}

function openInfoWindow() {
    infowindow.open(map,marker);
}

function mapZoom(location,zoom) {
    map.setZoom(zoom);
    map.setCenter(location);
}