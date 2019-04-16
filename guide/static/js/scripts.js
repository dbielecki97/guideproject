var directionsDisplay;
var directionsService;
function initMap() {
    directionsDisplay = new google.maps.DirectionsRenderer();
    directionsService = new google.maps.DirectionsService();
    var pb = data_from_django[0]
    var palac_branickich = new google.maps.LatLng(pb["lat"], pb["lgt"]);
    var mapOptions = {
        zoom: 15,
        center: palac_branickich
    }
    var map = new google.maps.Map(document.getElementById('map'), mapOptions);
    var marker = new google.maps.Marker({
        position: palac_branickich,
        map: map,
        title: "start"
    });
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
