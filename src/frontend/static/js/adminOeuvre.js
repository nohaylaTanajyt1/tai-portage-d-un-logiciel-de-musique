
function myfunction_onload(){
    console.log("Admin oeuvre : Chargé, déchargé");
}

// Fonction permettant la déconnection et la redirection vers la page de connexion
// Activer par le menu en haut à droite de la page video.js
function seDeconnecter() {
    window.location.href = '/connexion';
}

// Fonction permettant la redirection vers la page de menu Principal (choix des oeuvres)
// Activer par le menu de gauche de la page video.js
function modeAdmin() {
    window.location.href = '/menuPrincipal';
}

//Récupère les valeurs des champs html pour ajouter une nouvelle oeuvre dans la base de donnée (backend)
function boutonAjouterOeuvre() {
    var oeuvre = document.getElementById("oeuvre").value;
    var tonalite = document.getElementById("tonalite").value;
    var bpm = document.getElementById("bpm").value;
    var date_sortie = document.getElementById("date_sortie").value;
    var genre = document.getElementById("genre").value;
    var auteur = document.getElementById("auteur").value;
    
    //Requête Ajax vers /ajouterOeuvre (app.py)
    //Ajoute une nouvelle oeuvre grâce aux valeurs si dessus.
    $.ajax({
        type : "POST",
        url: "/ajouterOeuvre",
        data: {oeuvre : oeuvre, tonalite : tonalite, bpm : bpm, date_sortie : date_sortie, genre : genre, auteur : auteur}
    });
}

const btn2 = document.getElementById('annulerBtnOeuvre');

//Vide les valeurs des champs
//Appelé lorsqu'on clique sur annuler
btn2.addEventListener('click', function handleClick(event) {
    var oeuvre = document.getElementById("oeuvre");
    var tonalite = document.getElementById("tonalite");
    var bpm = document.getElementById("bpm");
    var date_sortie = document.getElementById("date_sortie");
    var genre = document.getElementById("genre");
    var auteur = document.getElementById("auteur");
    oeuvre.value = "";
    tonalite.value = "";
    bpm.value = "";
    date_sortie.value = "";
    genre.value = "";
    auteur.value = "";
});

const btn = document.getElementById('ajouterOeuvreBtn');

//Vide les valeurs des champs
//Appelé lorsqu'on clique sur ajouter
btn.addEventListener('click', function handleClick(event) {
    var oeuvre = document.getElementById("oeuvre");
    var tonalite = document.getElementById("tonalite");
    var bpm = document.getElementById("bpm");
    var date_sortie = document.getElementById("date_sortie");
    var genre = document.getElementById("genre");
    var auteur = document.getElementById("auteur");
    oeuvre.value = "";
    tonalite.value = "";
    bpm.value = "";
    date_sortie.value = "";
    genre.value = "";
    auteur.value = "";
});