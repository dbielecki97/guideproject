var directionsDisplay;
var directionsService;

function setMarkers(map, locations) {
    var marker, i
    for (i = 0; i < locations.length; i++) {
        var name = locations[i]['name']
        var lat = locations[i]['lat']
        var long = locations[i]['lgt']
        latlngset = new google.maps.LatLng(lat, long);
        console.log(latlngset);
        var marker = new google.maps.Marker({
            map: map, title: name, position: latlngset
        });
        var infowindow = new google.maps.InfoWindow()
        google.maps.event.addListener(marker, 'click', (function (marker, name, infowindow) {
            return function () {
                infowindow.setContent(name);
                infowindow.open(map, marker);
            };
        })(marker, name, infowindow));
    }
}


function initMap() {
    directionsDisplay = new google.maps.DirectionsRenderer();
    directionsService = new google.maps.DirectionsService();

    var bialystok = new google.maps.LatLng(53.12750505, 23.14705087);
    var mapOptions = {
        zoom: 12,
        center: bialystok,
        disableDefaultUI: true,
    }
    var map = new google.maps.Map(document.getElementById('map'), mapOptions);
    // for (var i in attractions) {
    //     var marker = new google.maps.Marker({
    //         position: new google.maps.LatLng(attractions[i]['lat'], attractions[i]['lgt']),
    //         map: map,
    //         animation: google.maps.Animation.DROP,
    //     });
    //     var contentString = '<div id="info">' +
    //         '<h1 id="firstHeading" class="firstHeading">' + attractions[i]['name'] + '</h1>' +
    //         '</div>';

    //     var infowindow = new google.maps.InfoWindow({
    //         content: contentString
    //     });

    //     google.maps.event.addListener(marker, 'click', (function (marker, infowindow) {
    //         return function () {
    //             infowindow.open(map, marker);
    //         };
    //     })(marker, content, infowindow));
    // }
    setMarkers(map, attractions);
    directionsDisplay.setMap(map);
    // calcRoute(map);
}

// function calcRoute(map) {
//     var start = new google.maps.LatLng(41.850033, -87.6500523);
//     var end = new google.maps.LatLng(37.3229978, -122.0321823);
//     var startMark = new google.maps.Marker({
//         position: start,
//         map: map,
//         title: "start"
//     });
//     var endMark = new google.maps.Marker({
//         position: end,
//         map: map,
//         title: "end"
//     });
//     var waypoints = [{ location: new google.maps.LatLng(44.986656, -93.258133) }, { location: new google.maps.LatLng(39.742043, -104.991531) }];
//     var request = {
//         origin: start,
//         destination: end,
//         travelMode: 'DRIVING',
//         waypoints: waypoints,

//     };
//     directionsService.route(request, function (response, status) {
//         if (status == 'OK') {
//             directionsDisplay.setDirections(response);
//         } else {
//             alert("directions request failed, status=" + status)
//         }
//     });
// }
google.maps.event.addDomListener(window, "load", initMap);
