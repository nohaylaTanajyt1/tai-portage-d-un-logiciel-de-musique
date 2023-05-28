//Objet regroupant les données à propos d'une oeuvre
//  id : id de l'oeuvre
//  artiste : artiste de l'oeuvre
//  nom : nom de l'oeuvre
//  path : chemin dans le repertoire vers l'oeuvre
class Oeuvre {
    constructor(artiste, nom, path, id) {
        this.id = id;
        this.artiste = artiste;
        this.nom = nom;
        this.path = path;
    }
}

//Renvoie l'oeuvre en fonction de son id
//Paramètre :   id : id de l'oeuvre souhaité
function getOeuvrebyId(id) {
    res = false;
    oeuvres.forEach(function (oeuvre) {
        if (oeuvre.id == id) {res = oeuvre} 
    });
    return res; 
}

//Tableau contenant toutes les oeuvres de la pages
var oeuvres = new Array();
var idOeuvre = 0;

//Retour a la page connexion
//Appelé par le menu du haut "se déconnecter" (html)
function seDeconnecter() {
    window.location.href = '/connexion';
}

//Permet d'aller sur la page d'ajout d'oeuvre
//Appelé par le menu du haut "mode administrateur" (html)
function modeAdmin() {
    window.location.href = '/adminOeuvre';
}

//Permet de se rendre sur la page video.html en passant en paramètre
//l'oeuvre cliqué.
//Paramètres :  destination : nom de la page
//              id : id de l'image sur laquelle on a cliqué dans le html (nom de l'oeuvre)
function allerA(destination, id) {
    oeuvre = getOeuvrebyId(id);

    //On met les variables en localStorage pour pouvoir les retrouver dans le js de video.js
    const artisteObj = { artiste: oeuvre.artiste};
    const nomObj = { nom: oeuvre.nom};
    const pathObj = { path: oeuvre.path};

    const artisteString = JSON.stringify(artisteObj);
    const nomString = JSON.stringify(nomObj);
    const pathString = JSON.stringify(pathObj);

    localStorage.setItem('artiste', artisteString);
    localStorage.setItem('nom', nomString);
    localStorage.setItem('path', pathString);

    window.location.href = '/' + destination;
}

//Ce lance au chargement de la page
function onLoad() {
    getOeuvre();
}

//Demande les oeuvres disponible au backend
function getOeuvre() {
    //Requête Ajax vers /getArtistes (app.py)
    //Renvoi un tableau d'oeuvre data
    $.ajax({
        type: "POST",
        url: "/getArtistes",
        success: function (data) {           
            afficherOeuvreDisponible(JSON.parse(data));
        }
    });
}

//Affiche et crée les objets oeuvres de toutes les oeuvres présentent dans data
//Paramètre :   data : Tableau d'oeuvre
function afficherOeuvreDisponible(data) {
    oeuvreDisponible = document.getElementById("oeuvreDisponible");
    code = " ";
    data.forEach(function (oeuvre) {
        artiste = oeuvre[5];
        nom = oeuvre[0];
        path = "../static/" + artiste + "/" + nom + "/";        
        id = "oeuvre" + idOeuvre++;

        oeuvres.push(new Oeuvre(artiste, nom, path, id));
        
        code += "<div class=\"thumbnail\"> <img id=\"" + id 
            //+ "\" class=\"thumbnail\""
            + "\" src=\"" + path + nom + ".jpg"
            + "\" onclick=\"allerA('video', this.id)\"></img>"
            + nom + "</div>";
    });
    oeuvreDisponible.innerHTML = code;
}