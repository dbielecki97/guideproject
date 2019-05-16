var directionsDisplay;
var directionsService;
var map
markers = []

function round(value, decimals = 0) {
    return Number(Math.round(value + 'e' + decimals) + 'e-' + decimals);
}

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
            $('#makeroute').click(() => { deleteMarkers(); calcRoute() });
        }
    }
}
function setMarkers(map, locs) {
    var marker, i, markersArray = []
    for (i = 0; i < locs.length; i++) {
        var name = locs[i]['name'];
        marker = setMarker(map, locs[i]);
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

function calcRoute() {
    waypoints = [];
    start = document.getElementById('start').value
    end = document.getElementById('end').value
    for (n = 0; n < locs.length; n++) {
        if (locs[n]['name'] == start || locs[n]['name'] == end)
            continue;
        waypoints.push({ 'location': locs[n]['lat-lng'], 'stopover': true })
    }
    var request = {
        origin: document.getElementById('start').value,
        destination: document.getElementById('end').value,
        waypoints: waypoints,
        travelMode: 'WALKING',
        optimizeWaypoints: true,
    };
    directionsService.route(request, function (response, status) {
        if (status == 'OK') {
            directionsDisplay.setDirections(response);
            var route = response.routes[0];
            totalWalkingTime = 0;
            totalWalkingDistance = 0;
            for (var i = 0; i < route.legs.length; i++) {
                totalWalkingDistance += route.legs[i]['distance']['value']
                totalWalkingTime += route.legs[i]['duration']['value']
            }
            hoursTag = document.getElementById('totalTime_hours');
            minutesTag = document.getElementById('totalTime_minutes');
            totalDistance = document.getElementById('totalDistance');
            totalDistance.innerHTML = "Całkowita droga do przejścia: " + round(totalWalkingDistance / 1000, 2) + " km";
            totalTime = hours + minutes / 60;
            totalTime += totalWalkingTime / 3600;
            console.log(totalTime)
            h = totalTime - totalTime % 1;
            m = round((totalTime - h) * 60)
            hoursTag.innerHTML = h;
            minutesTag.innerHTML = m;
        } else {
            alert("directions request failed, status=" + status)
        }
    });
}