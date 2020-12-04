mapboxgl.accessToken = 'pk.eyJ1IjoibHVjaWFuYWN0IiwiYSI6ImNrZnB1NzJzZjAyaTAyc213bzQzaW5xM2IifQ.g-6i_62u4jlDiZbf_kP7ew';
var map = new mapboxgl.Map({
container: 'map', // container id
style: 'mapbox://styles/lucianact/cki6fdpej73tw19p51oijfmwk', // style URL
center: [-122.446, 37.7653], // starting position [lng, lat]
zoom: 11 // starting zoom
});
// maps markers:
const doctorMarkers = [];
function showMap(url) {

    fetch(
        url
    ).then(
        response => response.json()
    ).then(
        doctors => {
            for (let marker of doctorMarkers) {
                marker.remove()
            }
            for (let doctor of doctors) {
                let marker = new mapboxgl.Marker()
                    .setLngLat([doctor.coordinates.longitude, doctor.coordinates.latitude])
                    .setPopup(new mapboxgl.Popup().setHTML(`<h5><a href="/doctor/${doctor.id}" class="doctor-links">${doctor.fullname}</a></h5><p><a href="https://www.google.com/maps/place/${doctor.address}" class="doctor-links">${doctor.address}</a><br>(click for directions)</p>`))
                    .addTo(map);
                doctorMarkers.push(marker);
            }
        }
    );
}
marker.togglePopup(); 