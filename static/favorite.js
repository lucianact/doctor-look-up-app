// function to bookmark and unbookmark doctors

const favoriteForm = document.getElementById('favorite');
const favoriteButton = document.getElementById('fav-button');

favoriteForm.addEventListener('submit', function (ev) {
    ev.preventDefault();

    fetch(favoriteForm.action, {method:'POST'}).then(response => response.json()).then(data => {
        if (data.isFavorited) {
            favoriteForm.action = "/unfavorite/{{doctor_id}}"
            favoriteButton.classList.add('favorite');
        } else {
            favoriteForm.action = "/favorite/{{doctor_id}}"
            favoriteButton.classList.remove('favorite');
        }
    })
    
});
