// create map object
var map = L.map('map').setView([48.683331, 6.2], 13);

// load map in
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

// create marker layer
var markerLayer = L.layerGroup().addTo(map);

// create markers
function createMarkersFromJSON(json) {
    obj = eval(json);
    for (building_index in obj) {
        var building = obj[building_index];
        var marker = L.marker([building.GPS_lat, building.GPS_long]).addTo(markerLayer);
        marker.bindPopup(building.building_name);
    }
}
fetch('/api/buildings')
    .then((response) => response.json())
    .then((json) => createMarkersFromJSON(json));