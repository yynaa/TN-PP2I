// create map object
var map = L.map('map').setView([48.683331, 6.2], 13);

// load map in
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

// create marker layer
var markerLayer = L.layerGroup().addTo(map);

var isPopupActive = false;

function openPopup() {
    document.getElementById("map").classList.add("popup-active");
    document.getElementById("popup").classList.add("popup-active");
    isPopupActive = true;
}

function closePopup() {
    document.getElementById("map").classList.remove("popup-active");
    document.getElementById("popup").classList.remove("popup-active");
    isPopupActive = false;
}

function togglePopup() {
    if (isPopupActive) {
        closePopup();
    }
    else {
        openPopup();
    }
}

function setMarkerData(id){
    fetch('/api/b/' + id)
        .then((response) => response.json())
        .then((json) => {
            document.getElementById("db-buildingname").innerHTML = json.building_name;
            document.getElementById("db-buildingdescription").innerHTML = json.class;
            document.getElementById("db-buildingaddress").innerHTML = json.address;
        });

}

// create markers
function createMarkersFromJSON(json) {
    obj = eval(json);
    for (building_index in obj) {
        var building = obj[building_index];
        var marker = L.marker([building.GPS_lat, building.GPS_long]).addTo(markerLayer);
        marker.on('click', function (e) {
            togglePopup();
            setMarkerData(building.building_id);
        });
    }
}
fetch('/api/buildings')
    .then((response) => response.json())
    .then((json) => createMarkersFromJSON(json));