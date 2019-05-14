var directionsDisplay;
var directionsService;
var map
markers = []
function setMapOnAll(map) {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(map);
    }
}
function clearMarkers() {
    setMapOnAll(null);
}
function deleteMarkers() {
    clearMarkers();
    markers = [];
}
function attractionList() {
    if (locs.length != 0) {
        initMap();
        setMarkers(map, locs);
        directionsDisplay.setMap(map)
    }
}
function attractionDetail() {
    if (loc[0]) {
        initMap(15, new google.maps.LatLng(loc[0]['lat-lng']));
        setMarker(map, loc[0]);
        directionsDisplay.setMap(map)
    }
}

function tripPlanDetail() {
    if (locs.length != 0) {
        initMap();
        markers = setMarkers(map, locs);
        directionsDisplay.setMap(map)
        if (locs.length >= 2) {
            waypoints = [];
            for (n = 1; n < locs.length - 1; n++) {
                waypoints.push({ 'location': locs[n]['lat-lng'], 'stopover': true })
            }
            start = locs[0]['lat-lng'];
            end = locs[locs.length - 1]['lat-lng'];
            $('#makeroute').click(() => { deleteMarkers(); calcRoute(start, end, waypoints) });
        }
    }
}
function setMarkers(map, locs) {
    var marker, i, markersArray = []
    for (i = 0; i < locs.length; i++) {
        var name = locs[i]['name'];
        marker = setMarker(map, locs[i], marker);
        markersArray.push(marker)
        var infowindow = new google.maps.InfoWindow()
        google.maps.event.addListener(marker, 'click', (function (marker, name, infowindow) {
            return function () {
                infowindow.setContent(name);
                infowindow.open(map, marker);
            };
        })(marker, name, infowindow));
    }
    return markersArray
}

function setMarker(map, loc) {
    var latlngset = new google.maps.LatLng(loc['lat-lng']);
    marker = new google.maps.Marker({
        map: map, name: loc['name'], position: latlngset,
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

function calcRoute(start, end, waypoints = []) {
    var startLatLng = new google.maps.LatLng(start);
    var endLatLng = new google.maps.LatLng(end);
    var request = {
        origin: startLatLng,
        destination: endLatLng,
        waypoints: waypoints,
        travelMode: 'WALKING',
        optimizeWaypoints: true,
    };
    directionsService.route(request, function (response, status) {
        if (status == 'OK') {
            directionsDisplay.setDirections(response);
        } else {
            alert("directions request failed, status=" + status)
        }
    });
}
