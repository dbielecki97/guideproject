var directionsDisplay;
var directionsService;
var map
function attractionList() {
    initMap();
    setMarkers(map, locs);
    directionsDisplay.setMap(map)
}
function attractionDetail() {
    initMap(15, new google.maps.LatLng(loc));
    setMarker(map, loc);
    directionsDisplay.setMap(map)
}
function setMarkers(map, locs) {
    var marker, i
    for (i = 0; i < locs.length; i++) {
        var name = locs[i]['name'];
        marker = setMarker(map, locs[i], marker);
        var infowindow = new google.maps.InfoWindow()
        google.maps.event.addListener(marker, 'click', (function (marker, name, infowindow) {
            return function () {
                infowindow.setContent(name);
                infowindow.open(map, marker);
            };
        })(marker, name, infowindow));
    }
}

function setMarker(map, loc, marker) {
    var latlngset = new google.maps.LatLng(loc['lat'], loc['lng']);
    marker = new google.maps.Marker({
        map: map, name: loc['name'], position: latlngset
    });
    return marker;
}

function initMap(zoom = 13, center = new google.maps.LatLng(53.12750505, 23.14705087)) {
    directionsDisplay = new google.maps.DirectionsRenderer();
    directionsService = new google.maps.DirectionsService();
    var mapOptions = {
        zoom: zoom,
        center: center,
        disableDefaultUI: true,
    }
    map = new google.maps.Map(document.getElementById('map'), mapOptions);
}

function calcRoute(map) {
    var start = new google.maps.LatLng(41.850033, -87.6500523);
    var end = new google.maps.LatLng(37.3229978, -122.0321823);
    var startMark = new google.maps.Marker({
        position: start,
        map: map,
        title: "start"
    });
    var endMark = new google.maps.Marker({
        position: end,
        map: map,
        title: "end"
    });
    var waypoints = [{ location: new google.maps.LatLng(44.986656, -93.258133) }, { location: new google.maps.LatLng(39.742043, -104.991531) }];
    var request = {
        origin: start,
        destination: end,
        travelMode: 'DRIVING',
        waypoints: waypoints,

    };
    directionsService.route(request, function (response, status) {
        if (status == 'OK') {
            directionsDisplay.setDirections(response);
        } else {
            alert("directions request failed, status=" + status)
        }
    });
}
