mapboxgl.accessToken = 'pk.eyJ1IjoibHVjaWFuYWN0IiwiYSI6ImNrZnB1NzJzZjAyaTAyc213bzQzaW5xM2IifQ.g-6i_62u4jlDiZbf_kP7ew';
var map = new mapboxgl.Map({
container: 'map', // container id
style: 'mapbox://styles/mapbox/streets-v11', // style URL
center: [-122.446, 37.7653], // starting position [lng, lat]
zoom: 8 // starting zoom
});

const doctorMarkers = [];

// const getDoctorSpecialty = document.querySelector('#get-doc-specialty');
const getDoctor = document.querySelector('#get-doctor');

getDoctor.addEventListener('submit', (evt) => { 
    // evt.preventDefault();
    let specialty = getDoctor.value;
    console.log(`/doctor-by-specialty/${specialty}`)


    fetch(
        `/doctor-by-specialty/${specialty}`
    ).then(
        response => response.json()
    ).then(
        doctors => {
            for (var marker of doctorMarkers) {
                marker.remove()
            }
            for (var doctor of doctors) {
                var marker = new mapboxgl.Marker()
                    .setLngLat([doctor.coordinates.longitude, doctor.coordinates.latitude])
                    .setPopup(new mapboxgl.Popup().setHTML(`<h1>${doctor.full_name}</h1><br><p>${doctor.address}`))
                    .addTo(map);
                doctorMarkers.push(marker);
            }
        }
    );
});
// marker.togglePopup(); 