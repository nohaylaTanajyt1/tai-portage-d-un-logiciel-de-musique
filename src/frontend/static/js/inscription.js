//Retourne à la page connexion.html
//Appelé par se connecter (html)
function retourConnexion() {
    $.ajax({
        type : "POST",
        url: "/inscription",
        success: function(res){
            window.location.href = "/connexion";
        }
    });
}

//Récupère les valeurs des champs html pour l'inscription et envoi une requete Ajax
//Si l'inscription est réussite -> retour à connexion, sinon -> affichage erreur
function boutonInscription() {
    var identifiant = document.getElementById("identifiant").value;
    var mdp = document.getElementById("mdp").value;
    var mail = document.getElementById("mail").value;
    var err = document.getElementById("errInscription");
    
    //Requête Ajax vers /créerCompte (app.py)
    //data :    identifiant, mot de passe, email
    //return :  ok si inscription réussite, string sinon 
    $.ajax({
        type : "POST",
        url: "/créerCompte",
        data: {id : identifiant, mdp : mdp, mail: mail},
        success: function(res){
            if (res === "ok")
            window.location.href = "/connexion";
            else
            err.innerHTML=res;
            //err.innerHTML="Mot de passe ou identifiant incorrect";
        }
    });
}

const btn = document.getElementById('annulerBtnInscr');

//Enlève les valeurs des champs
//Appelé par le bouton annuler (html)
btn.addEventListener('click', function handleClick(event) {
    var identifiant = document.getElementById("identifiant");
    var mdp = document.getElementById('mdp');
    identifiant.value = '';
    mdp.value = '';
    mail.value ='';
});

//Requete Ajax au chargement de la page
function myfunction_onload() {
    $.ajax({
        url: "/",
        context: document.body
    });
    console.log("page chargé");
}