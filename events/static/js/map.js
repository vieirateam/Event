var map;
var marker;
var inputLat;
var inputLng;

function initMap() {
    inputLat = document.getElementById("id_latitude");
    inputLng = document.getElementById("id_longitude");
    var page = document.getElementById("id_page");
    var mapCanvas = document.getElementById("map");

    var initialZoom = 7;
    var finalZoom = 13;

    if(page.value == "detail") {
        initialZoom = 16;
        finalZoom = 16;
        content = 'Latitude: ' + inputLat.value + '<br>Longitude: ' + inputLng.value;
    }

    var mapCenter = new google.maps.LatLng(inputLat.value,inputLng.value);
    var mapOptions = {center: mapCenter, zoom: initialZoom};
    map = new google.maps.Map(mapCanvas, mapOptions);

    if(page.value == "edit") {
        google.maps.event.addListener(map, 'click', function(event) {
            placeMarker(event.latLng);
        });
        var content = "Canoinhas";
    }

    addMarker(mapCenter);

    google.maps.event.addListener(marker,'click',function() {
        mapZoom(marker.getPosition(),finalZoom);
        addInfoWindow(content);
    });

    addInfoWindow(content);
}

function placeMarker(location) {
    mapZoom(location,16);
    marker.setMap(null);
    addMarker(location);

    var content = 'Latitude: ' + location.lat() + '<br>Longitude: ' + location.lng();
    addInfoWindow(content);

    google.maps.event.addListener(marker,'click',function() {
        addInfoWindow(content);
    });

    inputLat.value = location.lat();
    inputLng.value = location.lng();
}

function addMarker(location) {
    marker = new google.maps.Marker({
        position: location,
        map: map
    });
}

function addInfoWindow(content) {
    var infowindow = new google.maps.InfoWindow({
        content: content
    });
    infowindow.open(map,marker);
}

function mapZoom(location,zoom) {
    map.setZoom(zoom);
    map.setCenter(location);
}