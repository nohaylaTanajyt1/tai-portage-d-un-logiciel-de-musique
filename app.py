from flask import Flask, render_template, request, make_response
import mysql, mysql.connector, mido, json, jsonpickle, os

app = Flask(__name__, template_folder='./src/frontend/templates', static_folder='./src/frontend/static')
TEMPLATES_AUTO_RELOAD = True
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_UNIX_SOCKET'] = 'TCP'

import sys
sys.path.insert(0, './src/backend/mysql/login')
from utilisateurs import *
from administrateurs import *
from login import *

sys.path.append('./src/backend/application')
from pianoRoll import *
from parseJson import *

#Page de connexion de l'application
@app.route('/')
def index():
    return render_template('connexion.html')

#Cette fonction permet de tester le login et le mot de passe d'un utilisateur
#Elle est appelée lorsque l'on clique sur le bouton connexion de la page connexion.html
#Elle ne prend rien en entrée mais récupère par méthode POST l'id et le mot de passe
#Elle renvoie un code de connexion ou d'erreur suivant l'existance du couple (id, mdp) dans la bdd
@app.route('/testConnexion', methods=["POST"])
def testConnexion():
    login = request.form['id']
    password = request.form['mdp']
    idUser = getId(login)
    passw = hashlib.sha256(password.encode('utf-8')).hexdigest()

    if(idUser == None):
        resp = make_response('error: no login matched')
        resp.set_cookie('connected','false')
        return resp
    else:
        if (verifPass(idUser)[0] == passw):
            resp = make_response('ok')
            resp.set_cookie('connected', 'true')
            resp.set_cookie('login', login)
            return resp
        else: 
            resp = make_response('error: password incorrect')
            resp.set_cookie('connected','false')
            return resp

#Cette fonction permet d'envoyer au frontend la page connexion.html
#Elle permet de définir un cookie de connexion qui permet de savoir si l'utilisateur est connecté
@app.route('/connexion/', methods=["GET","POST"])
def connexion():
    resp = make_response(render_template('connexion.html'))
    resp.set_cookie('connected','false')
    return resp

#Cette fonction permet d'envoyer au frontend la page inscription.html
#Elle permet de définir un cookie de connexion qui permet de savoir si l'utilisateur est connecté
@app.route('/inscription/', methods=["GET","POST"])
def inscription():
    resp = make_response(render_template('inscription.html'))
    resp.set_cookie('connected','false')
    return resp

#Cette fonction permet de créer un compte en récupérant par méthode post le login, le password et le mail
#Elle renvoie un code d'erreur si le nom de compte est déjà existant ou "ok" lorsque le commpte est bien créé
#Elle change la barre d'erreur qui s'affiche lorsque l'on ne renseigne pas un des champs
@app.route('/créerCompte/',methods=["GET","POST"])
def créerCompte():
    login = request.form['id']
    password = request.form['mdp']
    mail = request.form['mail']
    #On récupère le login si le user existe déjà, sinon retourne None
    idUser = getId(login)
    #Hashage du mot de passe pour qu'il ne soit pas en clair dans la base de données
    passw = hashlib.sha256(password.encode('utf-8')).hexdigest()
    err = ["erreur: "]
    #Gestion des erreurs
    if(login == ""):
        err.append("Identifiant non renseigné")
    if(password == ""):
        err.append("Mot de passe non renseigné")
    if(mail == ""):
        err.append("Adresse mail non renseigné")
    #Permet de sauter une ligne entre chaque erreur
    if(login == "" or password == "" or mail == ""):
        err = "<br>".join(err)
        return err
    #On ne crée le compte que si le nom de compte n'existe pas déjà
    if(idUser == None):
        createAccount(login, passw, mail)
        return "ok"
    else:
        return "erreur: Nom de compte déjà existant"

#Cette fonction permet d'envoyer au frontend la page menuPrincipal.html
#Elle vérifie que la personne est bien connectée en vérifiant la valeur des cookies
@app.route('/menuPrincipal/', methods=["GET","POST"])
def menuPrincpal():
    print(request.cookies.get('connected'))
    if(request.cookies.get('connected') == "true"):
        return render_template('menuPrincipal.html')
    else:
        return render_template('connexion.html')

#Cette fonction permet d'envoyer au frontend la page menuPrincipal.html
#Elle vérifie que la personne est bien connectée en vérifiant la valeur des cookies
@app.route('/getArtistes', methods=["GET","POST"])
def getMenuArtistes():
    artistes = getArtistes()
    liste_artistes = []
    liste_menu = []
    #Remplit liste_artistes par tous les artistes
    for artiste in artistes:
        liste_artistes.append(artiste[0])
    #Pour chaque artiste, on récupère le path des oeuvres et l'artiste en question
    for el in liste_artistes:
        path = "src/frontend/static/" + el + "/oeuvres.json"
        oeuvres = getOeuvres(el)
        for oeuvre in oeuvres:
            liste_menu.append(getOeuvre(oeuvre[0],path))
    return jsonpickle.encode(liste_menu)

#Renvoie les pistes vidéos pour une oeuvre
#Récupère en entrée le nom de l'oeuvre et le nom de l'auteur
@app.route('/getVideo', methods=["GET","POST"])
def getMenuVideo():
    oeuvre = request.form['oeuvre']
    auteur = request.form['auteur']
    path = "src/frontend/static/" + auteur + "/" + oeuvre + "/pistes.json"
    oeuvre = getPistes(oeuvre, auteur)
    liste_pistes = []
    # Mise en forme du contenu que l'on va envoyer
    i = 0
    for piste in oeuvre:
        liste_pistes.append(oeuvre[i])
        i += 1
    #On ne peut renvoyer de liste vers le frontend, on utilise jsonpickle pour changer le format de la liste
    return jsonpickle.encode(liste_pistes)

#Cette fonction permet d'envoyer au frontend la page menuPrincipal.html
#Elle vérifie que la personne est bien connectée en vérifiant la valeur des cookies
@app.route('/video/', methods=["GET","POST"])
def synchro():
    if(request.cookies.get('connected') == "true"):
        return render_template('video.html')
    else:
        return render_template('connexion.html')

@app.route('/pianoRoll/', methods=["GET","POST"])
def pianoRoll():
    mid = mido.MidiFile('./src/frontend/static/Mozart/Mozart Quintet/Billy_Joel_-_Piano_Man.mid', clip=True)
    result_array = mid2arry(mid)
    return json.dumps(result_array.tolist())


#Permet d'ajouter une oeuvre et l'artiste s'il n'existe pas déjà
#Récupère en entrée le nom de l'oeuvre, la tonalité, les bpm, la date de sortie, le genre et l'auteur
@app.route('/ajouterOeuvre/', methods=["GET","POST"])
def ajouterOeuvreVideo():
    oeuvre = request.form['oeuvre']
    tonalite = request.form['tonalite']
    bpm = request.form['bpm']
    date_sortie = request.form['date_sortie']
    genre = request.form['genre']
    auteur = request.form['auteur']
    #Le path dans l'application pour le json des oeuvres d'un artiste sont construits à partir du nom de l'auteur
    path = "src/frontend/static/" + auteur + "/oeuvres.json"

    #Si le dossier n'existe pas, cela crée un dossier du nom de l'auteur 
    try:
        os.mkdir("src/frontend/static/"+auteur)
    except:
        print("auteur déjà existant")
    #Crée le fichier oeuvres.json s'il n'existe pas déjà
    try:
        file = open(path,"x")
        file.write("{}")
        file.close()
    except:
        print("le fichier existe déjà")
    #Crée un dossier pour l'oeuvre dans le dossier de l'auteur, ce dossier contiendra toutes pistes et informations nécessaires au bon fonctionnement
    try:
        os.mkdir("src/frontend/static/" + auteur + "/" + oeuvre)
        ajouterOeuvre(oeuvre,tonalite,bpm,date_sortie,genre,auteur,path)
        return "ok"
    except:
        print("erreur dans ajouterOeuvre")
        return "erreur dans ajouterOeuvre"
    
#Permet de récupérer les informations pour une oeuvre
#Récupère en entrée le nom de l'œuvre et de l'artiste
#Renvoie les informations de l'oeuvre
@app.route('/OeuvreInfo/', methods=["GET","POST"])
def getInfoOeuvre():
    oeuvre = request.form['oeuvre']
    auteur = request.form['auteur']
    path = "src/frontend/static/" + auteur + "/oeuvres.json"

    return(jsonpickle.encode(getOeuvre(oeuvre,path)))
    
#Permet de modifier les informations d'une oeuvre déjà existante
#Récupère en entrée le nom de l'oeuvre, la tonalité, les bpm, la date de sortie, le genre et l'auteur
@app.route('/modifOeuvreInfo/', methods=["GET","POST"])
def modifOeuvreInfo():
    oeuvre = request.form['oeuvre']
    tonalite = request.form['tonalite']
    bpm = request.form['bpm']
    date_sortie = request.form['date_sortie']
    genre = request.form['genre']
    auteur = request.form['auteur']
    #Le path dans l'application pour le json des oeuvres d'un artiste sont construits à partir du nom de l'auteur
    path = "src/frontend/static/" + auteur + "/oeuvres.json"
    modifierOeuvre(oeuvre,path,tonalite,bpm,date_sortie,genre)
    return "ok"

#Permet de renvoyer vers la page pour ajouter/supprimer des oeuvres
#Teste si l'utilisateur est un administrateur et s'il est connecté
@app.route('/adminOeuvre/', methods=["GET","POST"])
def adminOeuvreMenu():
    if(request.cookies.get('connected') == "true"):
        if(getIdA(request.cookies.get('login')) == getId(request.cookies.get('login'))):
            return render_template('adminOeuvre.html')
        else:
            return render_template('menuPrincipal.html')
    else:
        return render_template('connexion.html')

#Permet de renvoyer vers la page pour modifier une oeuvre déjà existante
#Teste si l'utilisateur est un administrateur et s'il est connecté
@app.route('/adminModifOeuvre/', methods=["GET","POST"])
def adminModifOeuvre():
    if(request.cookies.get('connected') == "true"):
        if(getIdA(request.cookies.get('login')) == getId(request.cookies.get('login'))):
            return render_template('adminModifOeuvre.html')
        else:
            return render_template('menuPrincipal.html')
    else:
        return render_template('connexion.html')



if __name__ == '__main__':
    # Use the provided PORT environment variable, or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='.0.0.0', port=port)
