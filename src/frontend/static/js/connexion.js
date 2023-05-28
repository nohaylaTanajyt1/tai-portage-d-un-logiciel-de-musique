//Recupère les valeurs de champs pour essayer de se connecter
//Appelé lorsqu'on clique sur connexion
function boutonConnexion() {
    var identifiant = document.getElementById("identifiant").value;
    var mdp = document.getElementById("mdp").value;
    var err = document.getElementById("erreur");

    //Requête Ajax vers /testConnexion (app.py)
    //Paramètres :  identifiant, mot de passe
    //Retour     :  Ok si connexion réussi, string sinon
    $.ajax({
        type : "POST",
        url: "/testConnexion",
        data: {id : identifiant, mdp : mdp},
        success: function(res){
            if (res === "ok")
            window.location.href = "/menuPrincipal";
            else
            err.innerHTML=res;
            //err.innerHTML="Mot de passe ou identifiant incorrect";
        }
    });
}

//Permet d'aller à inscription.html
//Appelé lorsqu'on clique sur s'inscrire (html)
function goInscription(){
    $.ajax({
        type : "POST",
        url: "/connexion",
        success: function(res){
            window.location.href = "/inscription";
        }
    });
}

const btn = document.getElementById('annulerBtn');

//Enlève les valeurs des champs
//Appelé par le bouton annuler (html)
btn.addEventListener('click', function handleClick(event) {
    var identifiant = document.getElementById("identifiant");
    var mdp = document.getElementById('mdp');
    identifiant.value = '';
    mdp.value = '';
});

//Requete Ajax au chargement de la page
function myfunction_onload() {
    $.ajax({
        url: "/",
        context: document.body
    });
    console.log("page chargé");
}