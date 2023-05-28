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

//A finir, c'est une fonction pour directement charger les données de l'oeuvre
//Appelé au chargement de la page
//Récupère les données du localStorage pour les mettre directement dans les champs html
function myfunction_onload(){
    var _o = document.getElementById("oeuvre");
    var _t = document.getElementById("tonalite");
    var _b = document.getElementById("bpm");
    var _d = document.getElementById("date_sortie");
    var _g = document.getElementById("genre");
    var _a = document.getElementById("auteur");

    _o.innerHTML = JSON.parse(localStorage.getItem('nom'));
    _t.value = JSON.parse(localStorage.getItem('tonalite'));
    _b.value = JSON.parse(localStorage.getItem('bpm'));
    _d.value = JSON.parse(localStorage.getItem('date_sortie'));
    _g.value = JSON.parse(localStorage.getItem('genre'));
    _a.innerHTML = JSON.parse(localStorage.getItem('auteur'));
}

const btn = document.getElementById('annulerBtnOeuvre');

//Reset les valeurs des champs 
//Appelé lorsqu'on clique sur annuler
btn.addEventListener('click', function handleClick(event) {
    myfunction_onload();
});

function goBack() {
    history.back();
  }
  
//Récupère les valeurs des champs pour modifier une oeuvre aua niveau backend
function boutonModifOeuvre(){
    var _o = document.getElementById("oeuvre").innerHTML;
    var _t = document.getElementById("tonalite").value;
    var _b = document.getElementById("bpm").value;
    var _d = document.getElementById("date_sortie").value;
    var _g = document.getElementById("genre").value;
    var _a = document.getElementById("auteur").innerHTML;
    
    //Requête Ajax vers /modifOeuvreInfo (app.py)
    //Modifie l'oeuvre souhaité avec les valeurs si dessus.
    $.ajax({
        type : "POST",
        url: "/modifOeuvreInfo",
        data: {oeuvre : _o, tonalite : _t, bpm : _b, date_sortie : _d, genre : _g, auteur : _a}
    });
}