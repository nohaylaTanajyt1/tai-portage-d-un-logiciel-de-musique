import json

path = "src/frontend/static/artistes.json"


#PARTIE ARTISTE

def ajouterArtiste(nom, epoque, genre):
    global path
    file = open(path, "r")   
    contenu = file.read()
    file.close()
    artistes = json.loads(contenu)
    try:
        test = getArtiste(nom)
    except:
        artistes[nom] = {"nom":nom, "oeuvre":[], "epoque":epoque, "genre":genre}
        file = open(path, "w")
        file.write(json.dumps(artistes))
        file.close()
    
def supprimerArtiste(nom):
    global path
    file = open(path, "r")   
    contenu = file.read()
    file.close()
    artistes = json.loads(contenu)
    del artistes[nom]
    file = open(path, "w")
    file.write(json.dumps(artistes))
    file.close()

def ajouterOeuvreArt(nom,oeuvre):
    global path
    file = open(path, "r")   
    contenu = file.read()
    file.close()
    artistes = json.loads(contenu)
    artistes[nom]["oeuvre"].append(oeuvre)
    file = open(path, "w")
    file.write(json.dumps(artistes))
    file.close()
    
def supprimerOeuvreArt(nom,oeuvre):
    global path
    file = open(path, "r")   
    contenu = file.read()
    file.close()
    artistes = json.loads(contenu)
    i = 0
    for el in artistes[nom]["oeuvre"]:
        if artistes[nom]["oeuvre"][i] == oeuvre:
            del artistes[nom]["oeuvre"][i]
        i += 1
    file = open(path, "w")
    file.write(json.dumps(artistes))
    file.close()
    
def getArtiste(nom):
    global path
    file = open(path, "r")   
    contenu = file.read()
    file.close()
    artistes = json.loads(contenu)
    artiste = [nom]
    artiste.append(artistes[nom]["oeuvre"])
    artiste.append(artistes[nom]["epoque"])
    artiste.append(artistes[nom]["genre"])
    return artiste
    
def modifierArtiste(nom,epoque ="",genre=""):
    global path
    artiste = getArtiste(nom)
    if epoque == "":
        epoque = artiste[2]
    if genre == "":
        genre = artiste[3]
    file = open(path, "r")   
    contenu = file.read()
    file.close()
    artistes = json.loads(contenu)
    artistes[nom]["epoque"] = epoque
    artistes[nom]["genre"] = genre
    file = open(path, "w")
    file.write(json.dumps(artistes))
    file.close()

def getArtistes():
    global path
    file = open(path, "r")   
    contenu = file.read()
    file.close()
    artistes = json.loads(contenu)
    liste_artiste = []
    for el in artistes:    
        artiste = []
        artiste.append(artistes[el]["nom"])
        artiste.append(artistes[el]["oeuvre"])
        artiste.append(artistes[el]["epoque"])
        artiste.append(artistes[el]["genre"])
        liste_artiste.append(artiste)
    return liste_artiste


#PARTIE OEUVRES

def ajouterOeuvre(nom, tonalite, bpm, date_sortie, genre, auteur, path):
    file = open(path, "r")
    contenu = file.read()
    file.close()
    oeuvres = json.loads(contenu)
    oeuvres[nom] = {"nom":nom, "tonalite": tonalite, "bpm":bpm, "date_sortie":date_sortie, "genre":genre, "auteur":auteur}
    file = open(path, "w")
    file.write(json.dumps(oeuvres))
    file.close()
    ajouterArtiste(auteur, date_sortie,genre)
    ajouterOeuvreArt(auteur,nom)
    
def supprimerOeuvre(nom,path):
    auteur = getOeuvre(nom,path)[5]
    file = open(path, "r")   
    contenu = file.read()
    file.close()
    oeuvres = json.loads(contenu)
    del oeuvres[nom]
    file = open(path, "w")
    file.write(json.dumps(oeuvres))
    file.close()   
    
    supprimerOeuvreArt(auteur,nom)
    
def getOeuvre(nom,path):
    file = open(path, "r")   
    contenu = file.read()
    file.close()
    oeuvres = json.loads(contenu)
    oeuvre = [nom]
    oeuvre.append(oeuvres[nom]["tonalite"])
    oeuvre.append(oeuvres[nom]["bpm"])
    oeuvre.append(oeuvres[nom]["date_sortie"])
    oeuvre.append(oeuvres[nom]["genre"])
    oeuvre.append(oeuvres[nom]["auteur"])
    
    return oeuvre
    
    
def modifierOeuvre(nom, path, tonalite="", bpm=0, date_sortie="", genre=""):
    oeuvre = getOeuvre(nom,path)
    if tonalite == "":
        tonalite = oeuvre[1]
    if bpm == 0:
        bpm = oeuvre[2]
    if date_sortie == "":
        date_sortie = oeuvre[3]
    if genre == "":
        genre = oeuvre[4]
    file = open(path, "r")   
    contenu = file.read()
    file.close()
    oeuvres = json.loads(contenu)
    oeuvres[nom]["tonalite"] = tonalite
    oeuvres[nom]["bpm"] = bpm
    oeuvres[nom]["date_sortie"] = date_sortie
    oeuvres[nom]["genre"] = genre
    file = open(path, "w")
    file.write(json.dumps(oeuvres))
    file.close()

def getOeuvres(auteur):
    path = "src/frontend/static/" + auteur + "/oeuvres.json"
    file = open(path, "r")   
    contenu = file.read()
    file.close()
    oeuvres = json.loads(contenu)
    liste_oeuvres = []

    
    for el in oeuvres:    
        if oeuvres[el]["auteur"] == auteur:
            oeuvre = []
            oeuvre.append(oeuvres[el]["nom"])
            oeuvre.append(oeuvres[el]["tonalite"])
            oeuvre.append(oeuvres[el]["date_sortie"])
            oeuvre.append(oeuvres[el]["genre"])
            oeuvre.append(oeuvres[el]["auteur"])
            liste_oeuvres.append(oeuvre)
        
    return liste_oeuvres


#PARTIE OEUVRE

def ajouterPiste(nom,audio,instrument, path):
    file = open(path, "r")
    contenu = file.read()
    file.close()
    pistes = json.loads(contenu)
    pistes[nom] = {"audio":audio, "instrument":instrument}
    file = open(path, "w")
    file.write(json.dumps(pistes))
    file.close()
    changeNbInstr(getNbInstr(path),path)
    
def supprimerPiste(nom,path):
    file = open(path, "r")
    contenu = file.read()
    file.close()
    pistes = json.loads(contenu)
    del pistes[nom]
    file = open(path, "w")
    file.write(json.dumps(pistes))
    file.close()
    changeNbInstr(getNbInstr(path),path)
    
def getPiste(nom,path):
    file = open(path, "r")   
    contenu = file.read()
    file.close()
    pistes = json.loads(contenu)
    piste = [nom]
    piste.append(pistes[nom]["audio"])
    piste.append(pistes[nom]["instrument"])
    
    return piste
    
def getNbInstr(path):
    file = open(path, "r")   
    contenu = file.read()
    file.close()
    pistes = json.loads(contenu)
    i = -1
    for piste in pistes:
        i += 1
    return(i)

def changeNbInstr(value,path):
    file = open(path, "r")
    contenu = file.read()
    file.close()
    pistes = json.loads(contenu)
    pistes["oeuvre"]["instruments"] = value
    file = open(path, "w")
    file.write(json.dumps(pistes))
    file.close()

def getPistes(oeuvre, auteur):
    path = "src/frontend/static/" + auteur + "/" + oeuvre + "/pistes.json"
    file = open(path, "r")   
    contenu = file.read()
    file.close()
    pistes = json.loads(contenu)
    liste_pistes = []
    liste_pistes.append(pistes["oeuvre"]["video"])
    liste_pistes.append(pistes["oeuvre"]["instruments"])
    for el in pistes:
        if el != "oeuvre":
            liste_pistes.append(pistes[el])

    return liste_pistes


#PARTIE STRUCTURE


def getStructure(oeuvre, auteur):
    path = "src/frontend/static/" + auteur + "/" + oeuvre + "/structure.json"
    file = open(path, "r")   
    contenu = file.read()
    file.close()
    structure = json.loads(contenu)
    liste_parties = []
    for partie in structure:
        p = [partie]
        for section in structure[partie]:
            s = [section]
            for ssection in structure[partie][section]:
                ss = [ssection]
                ss.append(structure[partie][section][ssection])
                s.append(ss)
            p.append(s)
        liste_parties.append(p)
    return(liste_parties)

#Permet d'ajouter ou modifier une sous section 
def ajouterSsection(path,partie,section,ssection,start,end):
    file = open(path, "r")
    contenu = file.read()
    file.close()
    structure = json.loads(contenu)
    structure[partie]={section:ssection}
    structure[partie][section] = {ssection:[start,end]}
    file = open(path, "w")
    file.write(json.dumps(structure))
    file.close()

def enleverSsection(path,partie,section,ssection):
    file = open(path, "r")
    contenu = file.read()
    file.close()
    structure = json.loads(contenu)
    del structure[partie][section][ssection]
    file = open(path, "w")
    file.write(json.dumps(structure))
    file.close()

def enleverSection(path,partie,section):
    file = open(path, "r")
    contenu = file.read()
    file.close()
    structure = json.loads(contenu)
    del structure[partie][section]
    file = open(path, "w")
    file.write(json.dumps(structure))
    file.close()

def enleverPartie(path,partie,section):
    file = open(path, "r")
    contenu = file.read()
    file.close()
    structure = json.loads(contenu)
    del structure[partie]
    file = open(path, "w")
    file.write(json.dumps(structure))
    file.close()

def modifNomPartie(path,oldpartie,newpartie):
    file = open(path, "r")
    contenu = file.read()
    file.close()
    structure = json.loads(contenu)
    mem = structure[oldpartie]
    del structure[oldpartie]
    structure[newpartie] = mem
    file = open(path, "w")
    file.write(json.dumps(structure))
    file.close()

def modifNomSection(path,partie,oldsection,newsection):
    file = open(path, "r")
    contenu = file.read()
    file.close()
    structure = json.loads(contenu)
    mem = structure[partie][oldsection]
    del structure[partie][oldsection]
    structure[partie][newsection] = mem
    file = open(path, "w")
    file.write(json.dumps(structure))
    file.close()

def modifNomSsection(path,partie,section,oldssection,newssection):
    file = open(path, "r")
    contenu = file.read()
    file.close()
    structure = json.loads(contenu)
    mem = structure[partie][section][oldssection]
    del structure[partie][section][oldssection]
    structure[partie][section][newssection] = mem
    file = open(path, "w")
    file.write(json.dumps(structure))
    file.close()