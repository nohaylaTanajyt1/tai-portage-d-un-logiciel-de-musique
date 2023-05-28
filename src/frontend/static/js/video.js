// Fonction permettant la déconnection et la redirection vers la page de connexion
// Activer par le menu en haut à droite de la page video.js
function seDeconnecter() {
    window.location.href = '/connexion';
}

// Fonction permettant la redirection vers la page de menu Principal (choix des oeuvres)
// Activer par le menu de gauche de la page video.js
function retourMenuPrincipal() {
    $.ajax({
        type: "POST",
        url: "/video",
        success: function (res) {
            window.location.href = "/menuPrincipal";
        }
    });
}

function modeAdmin() {
    //passe en mode administrateur

    var tonalite, oeuvre_bpm, date_sortie, genre;

    $.ajax({
        type: "POST",
        url: "/OeuvreInfo/",
        data: { oeuvre: oeuvre.nom, auteur: oeuvre.artiste },
        success: function (res) {
            parsed = JSON.parse(res)
            console.log(parsed);
            tonalite = parsed[1];
            oeuvre_bpm = parsed[2];
            date_sortie = parsed[3];
            genre = parsed[4];
            localStorage.setItem('nom', JSON.stringify(oeuvre.nom));
            localStorage.setItem('tonalite', JSON.stringify(tonalite));
            localStorage.setItem('bpm', JSON.stringify(oeuvre_bpm));
            localStorage.setItem('date_sortie', JSON.stringify(date_sortie));
            localStorage.setItem('genre', JSON.stringify(genre));
            localStorage.setItem('auteur', JSON.stringify(oeuvre.artiste));
        }

    });

    $.ajax({
        type: "POST",
        url: "/video",
        success: function (res) {

            window.location.href = '/adminModifOeuvre';
        }
    });

}

let idInput = 0;
let idAudio = 0;
let videoDisplay = false;
let video = document.getElementById("zone_video");

//Class Oeuvre : regroupe tous les élements a afficher par rapport à l'oeuvre.
//  nombreInstrument : nombre de pistes audio de l'oeuvre
//  audios : tableau contenant les pistes audios
//  analyse : tableau contenant l'analyse
//  path : chemin dans les fichiers : ../static/[artiste]/[oeuvre]/
//  text : text du fichier
class Oeuvre {
    constructor() {
        this.nombreInstrument = 0;
        this.audios = new Array();
        this.analyse = new Array();
    }

    setNom(nom) { this.nom = nom }
    setArtiste(artiste) { this.artiste = artiste }
    setPath(path) { this.path = path }

    ajouterPisteAudio(audio) {
        this.audios.push(audio);
    }

    ajouterAnalyse(analyse) {
        this.analyse = analyse;
    }

    ajouterText(text) {
        this.text = text;
    }
}

//Information a propos des piste audios de l'oeuvre.
//  id : id de la piste audio
//  name : nom de la piste audio -> nom du bouton
class pisteAudio {
    constructor(name, url) {
        this.id = idAudio++;
        this.name = name;
        this.audio = new Audio(url);
        this.ancienVolume = 0;
        this.mute = false;
    }
}

//Contient toutes les parties->sections->sousSections.
//  parties : Array de Partie
//  debut : debut de l'analyse en seconde (timecode) (0)
//  fin : fin de l'analyse en seconde (timecode)
class Analyse {
    constructor() {
        this.parties = new Array();
    }

    ajouterPartie(partie) {
        this.parties.push(partie);
        this.debut = this.parties[0].debut;
        this.fin = this.parties[this.parties.length - 1].fin;
    }
}

//Contient des sections->sousSections
//  id : id de la partie
//  nom : nom de la partie (nom affiché)
//  sections : Array de Section
//  debut : debut de la partie (timecode en s), timecode de la première section.
//  fin : fin de la partie (timecode en s), timecode de la dernière section.
class Partie {
    constructor(nom, debut, fin) {
        this.id = idInput++;
        this.nom = nom;
        this.debut = debut;
        this.fin = fin;
        this.sections = new Array();
    }

    ajouterSection(section) {
        this.sections.push(section);
        this.debut = this.sections[0].debut;
        this.fin = this.sections[this.sections.length - 1].fin;
    }
}

//Contient des sousSections
//  id : id de la section
//  nom : nom de la section (nom affiché)
//  sousSections : Array de SousSections
//  debut : debut de la section (timecode en s), timecode de la première sousSection.
//  fin : fin de la section (timecode en s), timecode de la dernière sousSection.
class Section {
    constructor(nom, debut, fin) {
        this.id = idInput++;
        this.nom = nom;
        this.debut = debut;
        this.fin = fin;
        this.sousSections = new Array();
    }

    ajouterSousSection(sousSection) {
        this.sousSections.push(sousSection);
        this.debut = this.sousSections[0].debut;
        this.fin = this.sousSections[this.sousSections.length - 1].fin;
    }
}

//Sous section de l'analyse de l'oeuvre (ex : A1 A2 ...)
//  id : id de la sous section
//  nom : nom de la sous section (nom affiché)
//  debut : timecode en s correspondant au début de la sous section 
//  fin : timecode en s correspondant à la fin de la sous section
class SousSection {
    constructor(nom, debut, fin) {
        this.id = idInput++;
        this.nom = nom;
        this.debut = debut;
        this.fin = fin;
    }
}

// Permet de relancer des fonctions toutes les 10 ms
setInterval(setIntervalFunction, 10);
function setIntervalFunction() {
    if (videoDisplay == true) {
        affichageTemps();
        cssAnalyse();
    }
    drawNotes();
}

//Création de l'objet Oeuvre contenant toutes les informations sur l'oeuvre actuelle
oeuvre = new Oeuvre();
let analyse = new Analyse();
function onLoad() {
    //Récupération des données localStorage
    const artisteString = localStorage.getItem("artiste");
    const nomString = localStorage.getItem("nom");
    const pathString = localStorage.getItem("path");

    const artisteObj = JSON.parse(artisteString);
    const nomObj = JSON.parse(nomString);
    const pathObj = JSON.parse(pathString);

    //Attribution des valeurs
    creationOeuvre(artisteObj["artiste"], nomObj["nom"], pathObj["path"]);
    creationAnalyse();

    //Display de l'interface
    document.getElementById("titreOeuvre").innerHTML = oeuvre.nom;
    document.getElementById("interface").style.display = "inline-grid";
    document.getElementById("partition").style.display = "none";
    document.getElementById("pianoRoll").style.display = "none";
    document.getElementById("text").style.display = "none";
    document.getElementById("analyseBtn").style.backgroundColor = "lightblue";
    document.getElementById("interface").style.display = "inline-grid";

    textAffichage();

    //Affichage de la vidéo.
    // drawImge();
    console.log(oeuvre);
}

//Récupère les informations nécessaire de l'oeuvre
function creationOeuvre(artiste, nom, path) {
    oeuvre.artiste = artiste;
    oeuvre.nom = nom;
    oeuvre.path = path;

    //Requete Ajax /getvideo
    //  Paramètres : nom de l'oeuvre, auteur de l'oeuvre
    //  Retour : [NomDeLaVidéo.mp4, nombreInstruments, pisteAudio1, pisteAudio2, ...] 
    $.ajax({
        type: "POST",
        url: "/getVideo",
        data: { oeuvre: oeuvre.nom, auteur: oeuvre.artiste },
        success: function (data) {
            datajson = JSON.parse(data);
            video.insertAdjacentHTML('afterbegin', "<video id=\"video\" src=\" " + oeuvre.path + datajson[0] + "\"></video><canvas id=\"videoCanvas\"></canvas>");
            oeuvre.video = document.getElementById("video");

            //Création des audios de oeuvre/
            datajson.forEach(function (piste) {
                if (piste["audio"] != null) {
                    oeuvre.ajouterPisteAudio(new pisteAudio(piste["instrument"], oeuvre.path + piste["audio"]));
                }
            });
            oeuvre.nombreInstrument = datajson[1];
            videoDisplay = true;

            muteInstrumentAffichage();
            drawImge();
            pianoRollInit();
        }
    });

    //récupération nom de l'analyse
    // $.ajax({
    //     type: "POST",
    //     url: "/getAnalyseOeuvre",
    //     success: function (data) {
    //         //
    //     }
    // });
}

//Créer automatiquement la partie Analyse (avec les boutons)
//La fonction utilise actuellement des données en local (fct localAnalyse), il faut la modifier
//pour quelle prenne des données venant de la base de données (faudra faire des requetes Ajax).
function creationAnalyse() {
    localAnalyse();
    let zonePartie = document.getElementById("zone_partie");

    codePartie = "";
    //Parties
    oeuvre.analyse.parties.forEach(function (ePartie) {
        codeSection = "";
        codePartie += "<div class=\"partieDiv\"><input type=\"button\" id=\"" + ePartie.id + "\" class=\"sectionBoutton\" value=\"" + ePartie.nom + "\"onclick=\"setTime(" + ePartie.debut + ")\" />";

        //Sections
        ePartie.sections.forEach(function (eSection) {
            codeSousSection = "";
            codeSection += "<div class=\"sectionDiv\"><input type=\"button\" id=\"" + eSection.id + "\" class=\"sectionBoutton\" value=\"" + eSection.nom + "\"onclick=\"setTime(" + eSection.debut + ")\" />";

            //SousSections
            eSection.sousSections.forEach(function (eSousSection) {
                codeSousSection += "<div class=\"sousSectionDiv\"><input type=\"button\" id=\"" + eSousSection.id + "\" class=\"sousSectionBoutton\" value=\"" + eSousSection.nom + "\"onclick=\"setTime(" + eSousSection.debut + ")\" /></div>";
            });
            codeSection += codeSousSection + "</div>";
        });
        codePartie += codeSection + "</div>";
    });
    zonePartie.innerHTML = codePartie;
}

//Fonction temporaire. Création manuelle de l'analyse.
//Il faudra récupérer les données d'un fichier JSON du backend
function localAnalyse() {
    var ssA1 = new SousSection("A1", 0, 23);
    var ssA2 = new SousSection("A2", 24, 28);
    var ssB1 = new SousSection("B1", 29, 39);
    var ssB2 = new SousSection("B2", 40, 63);
    var ssC1 = new SousSection("C1", 64, 71);
    var ssC2 = new SousSection("C2", 72, 84);
    var ssC3 = new SousSection("C3", 85, 90);
    var ssC4 = new SousSection("C4", 91, 95);
    var ssD1 = new SousSection("D1=A", 96, 105);
    var ssD2 = new SousSection("D2=B", 106, 124);
    var ssD3 = new SousSection("D3=C", 125, 132);
    var ssA1R = new SousSection("A1", 133, 161);
    var ssA2R = new SousSection("A2", 162, 167);
    var ssB1R = new SousSection("B1", 168, 175);
    var ssB2R = new SousSection("B2", 176, 200);
    var ssC1R = new SousSection("C1", 201, 203);
    var ssC2R = new SousSection("C2", 204, 221);
    var ssC3R = new SousSection("C3", 222, 227);
    var ssC4R = new SousSection("C4", 228, 234);
    var ssE1 = new SousSection("E1=A1", 235, 242);
    var ssE2 = new SousSection("E2=B1", 243, 260);

    var s1 = new Section("Section 1");
    var s2 = new Section("Section 2");
    var s3 = new Section("Section 3");
    var s4 = new Section("Section 4");
    var s5 = new Section("Section 5");
    var s6 = new Section("Section 6");
    var s7 = new Section("Section 7");
    var s8 = new Section("Section 8");
    var s9 = new Section("Section 9");
    var s10 = new Section("Section 10");
    s1.ajouterSousSection(ssA1);
    s1.ajouterSousSection(ssA2);
    s2.ajouterSousSection(ssB1);
    s2.ajouterSousSection(ssB2);
    s3.ajouterSousSection(ssC1);
    s3.ajouterSousSection(ssC2);
    s3.ajouterSousSection(ssC3);
    s3.ajouterSousSection(ssC4);
    s4.ajouterSousSection(ssD1);
    s5.ajouterSousSection(ssD2);
    s5.ajouterSousSection(ssD3);
    s6.ajouterSousSection(ssA1R);
    s6.ajouterSousSection(ssA2R);
    s7.ajouterSousSection(ssB1R);
    s7.ajouterSousSection(ssB2R);
    s8.ajouterSousSection(ssC1R);
    s8.ajouterSousSection(ssC2R);
    s8.ajouterSousSection(ssC3R);
    s8.ajouterSousSection(ssC4R);
    s9.ajouterSousSection(ssE1);
    s10.ajouterSousSection(ssE2);

    var p1 = new Partie("EXPOSITION");
    var p2 = new Partie("DEVELOPPEMENT");
    var p3 = new Partie("REEXPOSITION");
    var p4 = new Partie("CODA");
    p1.ajouterSection(s1);
    p1.ajouterSection(s2);
    p1.ajouterSection(s3);
    p2.ajouterSection(s4);
    p2.ajouterSection(s5);
    p3.ajouterSection(s6);
    p3.ajouterSection(s7);
    p3.ajouterSection(s8);
    p4.ajouterSection(s9);
    p4.ajouterSection(s10);

    analyse.ajouterPartie(p1);
    analyse.ajouterPartie(p2);
    analyse.ajouterPartie(p3);
    analyse.ajouterPartie(p4);

    oeuvre.ajouterAnalyse(analyse);
}

//Permet de créer le menu de droite pour mute les différents instruments.
//Important :   Les boutons correspondent aux musiciens dans l'ordre 
//              La première piste audio du fichier json correspondra au musicien de gauche...
function muteInstrumentAffichage() {
    var muteInstrument = document.getElementById("muteInstrument");
    code = "";
    oeuvre.audios.forEach(function (audio) {
        code += "<input class=\"instru\" type=\"button\" id=\"audioInput" + audio.id + "\" value=\"" + audio.name + "\" onclick=\"mute(this.id)\" />";
    });
    muteInstrument.innerHTML = code;
}

//Affiche un timer en dessous de la vidéo
function affichageTemps() {
    const temps = document.getElementById("zone_temps");
    temps.innerHTML = oeuvre.video.currentTime.toFixed(2) + "s";
}

//Appelé par le bouton Play
//Synchronise les audios sur la vidéo puis play les audios + vidéos
function play() {
    videoAudioSynchro();
    oeuvre.video.play();
    oeuvre.audios.forEach(function (element) {
        element.audio.play();
    });
}

//Appelé par le bouton Stop
//Stop les audios + vidéos
async function stop() {
    oeuvre.video.pause();
    oeuvre.audios.forEach(function (element) {
        element.audio.pause();
    });
}

//Récupère le timer actuel de la vidéo pour synchroniser les pistes audios dessus
function videoAudioSynchro() {
    oeuvre.audios.forEach(function (element) {
        element.audio.currentTime = oeuvre.video.currentTime;
    });
}

//Avance de 10s la vidéo puis synchronise les pistes audios sur la vidéo
function avanceRapide() {
    oeuvre.video.currentTime = oeuvre.video.currentTime + 10;
    videoAudioSynchro();
}

//Recule de 10s la vidéo puis synchronise les pistes audios sur la vidéo
function reculRapide() {
    oeuvre.video.currentTime -= 10;
    videoAudioSynchro();
}

//Appelé généralement par les boutons de la partie analyse
//Permet de mettre la vidéo à un timer spécifique puis synchronise les pistes audios
//Paramètres :  time : nouveau timecode en ms 
function setTime(time) {
    oeuvre.video.currentTime = time;
    videoAudioSynchro();
}

//Text dans la section zone_text
//Il est en brut actuellement, mais à terme il faut le récupérer de la bdd ou d'un json ou d'un txt 
//(normalement une fonction en backend est prévu à cet effet)
function textAffichage() {
    var zoneText = document.getElementById("zone_text");
    text = "<p>Les deux Quintettes, en ut Majeur (K. 515) et en sol mineur (K. 516), pour deux violons, deux altos et violoncelle, sont écrits à quelques semaines d'intervalle et il est de coutume de les comparer. "
        + "Autant celui en ut Majeur respire la joie, la confiance, la sérénité et la majesté, autant le Quintette en sol mineur est l'expression d'une angoisse et d'un désarroi profonds. C'est certainement le plus réussi et le plus expressif des quintettes de Mozart : fait unique dans la musique classique instrumentale, il comporte deux mouvements lents (adagio ma non troppo / adagio) qui sont parmi les plus belles pages de la musique de chambre. "
        + "Ce quintette est exceptionnel par son invention mélodique, la conduite de la phrase, sa noblesse, sa hauteur intellectuelle et musicale. </p>"

    text += "<p>Pourquoi Mozart revient-il au quintette à cordes, genre qu'il avait délaissé quatorze ans plus tôt ? Celui pour deux violons, deux altos et violoncelle en si bémol Majeure (K. 174), daté de décembre 1773, est une œuvre de jeunesse dont le modèle lui aurait été donné par Michel Haydn (jeune frère de Joseph Haydn). "
        + "Le quintette est alors un genre nouveau dont le style s'apparente davantage au divertissement ou à la musique de plein air qu'à la musique de chambre authentique telle qu'elle s'exprime de façon intériorisée dans le quatuor. En 1787, Mozart a mûri : il est avant tout un compositeur lyrique de génie dont les opéras sont des sommets du genre. Il excelle également dans le concerto et a déjà écrit beaucoup de musique de chambre, des quatuors en particulier. "
        + "On sait d'autre part que Mozart aime jouer de l'alto et participe, en 1785, aux séances de quatuor qu'organise Nancy Storace : Mozart y tient l'alto, Joseph Haydn le second violon, Carl Ditters von Dittersdorf, le premier violon et le compositeur viennois Johann Baptist Wanhal, le violoncelle. </p>"

    text += "<p>Le quintette à cordes est un quatuor à corde avec second alto 'ajouté'. Le second alto aide à la transparence générale du morceau. Il libère le premier alto, celui du quatuor, de sa fonction accompagnatrice lorsque celui-ci a des parties solistes. Le premier alto peut donc chanter tandis que le second alto prend la place de l'alto normal, aux côtés du second violon. "
        + "Cette écriture à cinq, à la fois intime et concertante, permet à Mozart d'exprimer la quintessence de sa pensée en tant que compositeur de musique de chambre. "
        + "En avril 1788, le quintette en sol mineur fera partie d'une série de trois quintettes (Ut K. 515, sol K. 516 et ut K. 406, ce dernier étant une transcription de la Sérénade K. 388) pour lesquels Mozart ouvre une souscription en espérant gagner ainsi un peu d'argent et rétablir sa situation financière alarmante. "

    zoneText.innerHTML = text;
}

//Appelé par le menu de droite avec le nom des instruments.
//Permet de mute les instruments séparément en fct de leur id (audioInput + id)
//Paramètre :   id : id du bouton instrument cliqué dans le html 
function mute(id) {
    oeuvre.audios.forEach(function (element) {
        if (id == "audioInput" + element.id) {
            if (element.audio.volume > 0) {
                document.getElementById(id).style.backgroundColor = "darkgrey";
                document.getElementById(id).style.outline = "2px solid dark";
                element.ancienVolume = element.audio.volume;
                element.audio.volume = 0;
                element.mute = true;
            }
            else {
                element.audio.volume = element.ancienVolume;
                element.ancienVolume = 0;
                element.mute = false;
                document.getElementById(id).style.backgroundColor = "";
            }
        }
    });
}

//Affiche la section demandé (en dessous de la vidéo) grâce au menu de gauche (les icones)
//Paramètre :   id : id du bouton cliqué dans le html
function affichageSection(id) {
    document.getElementById("analyseBtn").style.backgroundColor = "";
    document.getElementById("partitionBtn").style.backgroundColor = "";
    document.getElementById("pianoRollBtn").style.backgroundColor = "";
    document.getElementById("textBtn").style.backgroundColor = "";

    document.getElementById("interface").style.display = "none";
    document.getElementById("partition").style.display = "none";
    document.getElementById("pianoRoll").style.display = "none";
    document.getElementById("text").style.display = "none";
    switch (id) {
        case 'analyseBtn':
            document.getElementById("interface").style.display = "inline-grid";
            break;
        case 'partitionBtn':
            document.getElementById("partition").style.display = "inline-grid";
            break;
        case 'pianoRollBtn':
            document.getElementById("pianoRoll").style.display = "inline-grid";
            break;
        case 'textBtn':
            document.getElementById("text").style.display = "inline-grid";
            break;
        default:
            console.log("Error bouton mute");
    }
    document.getElementById(id).style.backgroundColor = "lightblue";
}

//Fonction permettant de dessiner les caches noirs lorsqu'on mute une piste audio. 
//Pour que ça fonction il faut que la vidéo soit un canvas
async function drawImge() {
    var canvas = document.querySelector("#videoCanvas");
    var ctx = canvas.getContext('2d');

    canvas.width = oeuvre.video.videoWidth;
    canvas.height = oeuvre.video.videoHeight;

    //La hauteur du cache fera toujours 4.9 (norme pour la vidéo)
    //La largeur dépend du nombre de pistes audios de l'oeuvre
    hauteurInstrument = oeuvre.video.videoHeight / 4.9;
    largeurInstrument = oeuvre.video.videoWidth / oeuvre.nombreInstrument;

    ctx.drawImage(oeuvre.video, 0, 0, canvas.width, canvas.height);

    var i = 0;
    oeuvre.audios.forEach(function (eAudio) {
        if (eAudio.mute == true) {
            ctx.rect(largeurInstrument * i, 0, largeurInstrument, hauteurInstrument);
        }
        else {
            ctx.drawImage(oeuvre.video, 0, 0, canvas.width, canvas.height);
        }
        i++;
    });
    ctx.fill();
    if (canvas.width != 0)
        oeuvre.video.style.display = "none";
    setTimeout(drawImge, 100);
}

//Gère le css de la section Analyse 
//Met les boutons en surbrillance si le timecode de la vidéo correspond au timecode de la Partie/Section/SousSection
function cssAnalyse() {
    temps = oeuvre.video.currentTime;
    analyse.parties.forEach(function (ePartie) {
        if (ePartie.debut <= temps && ePartie.fin >= temps) {
            document.getElementById(ePartie.id).style.backgroundColor = "lightblue";
            document.getElementById(ePartie.id).style.outline = "2px solid dark";
        }
        else {
            document.getElementById(ePartie.id).style.backgroundColor = "";
        }
        ePartie.sections.forEach(function (eSection) {
            if (eSection.debut <= temps && eSection.fin >= temps) {
                document.getElementById(eSection.id).style.backgroundColor = "lightblue";
                document.getElementById(eSection.id).style.outline = "2px solid dark";
            }
            else {
                document.getElementById(eSection.id).style.backgroundColor = "";
            }
            eSection.sousSections.forEach(function (eSousSection) {
                if (eSousSection.debut <= temps && eSousSection.fin >= temps) {
                    document.getElementById(eSousSection.id).style.backgroundColor = "lightblue";
                    document.getElementById(eSousSection.id).style.outline = "2px solid dark";
                }
                else {
                    document.getElementById(eSousSection.id).style.backgroundColor = "";
                }
            });
        });
    });

}

video.onplay = function () {
    setTimeout(drawImge, 300);
}


//Partie pianoRoll
document.getElementById("pianoRoll").innerHTML = "<canvas id=\"pianoRollCanvas\"></canvas>";
var canvas = document.getElementById('pianoRollCanvas');
resizeCanvasToDisplaySize(canvas);
var vectorPianoRoll;

var ctx = canvas.getContext("2d");
//Hauteur Largeur du piano roll
var w = canvas.scrollWidth;
var h = canvas.scrollHeight;
var cellwidth, cellheight;

//Interval du tableau des vecteurs
var intervDebut, intervFin;

function pianoRollInit() {
    return new Promise(function (resolve, reject) {
        //Requete Ajax vers /pianoRoll
        //Récupère un tableau data de vecteur obtenu d'un fichier midi
        //Ce tableau contient des vecteurs de vecteur de int : [chaque note joué][chaque note joué à l'instant t] 
        $.ajax({
            type: "POST",
            url: "/pianoRoll",
            success: function (data) {
                vectorPianoRoll = JSON.parse(data);
                resolve(data);
            },
            error: function (err) {
                reject(err);
            }
        });
    });
}


//data.length = nombre de notes du morceaux
//data[x].length = 88 (chaque cas correspond a une touche d'un piano)
//data[x][x] = vélocité de la note : 0 la note n'est pas joué, != 0 la note est jouée 
pianoRollInit().then(function (data) {
    cellwidth = w / 80;
    cellheight = h / vectorPianoRoll[0].length;

    //on affiche 80 vecteurs du morceau en meme temps
    intervDebut = 0;
    intervFin = 80
    drawPianoGrid();
    var x, y;

    for (var x = intervDebut; x < intervFin; x++) {
        y = 0;
        vectorPianoRoll[x].forEach(function (e) {
            if (e != 0) {
                if (x == 1) { drawNote(x, y, 1, true); }
                else { drawNote(x, y, 1); }
            }
            y++;
        });
    };

    intervDebut++;
    intervFin++;
}).catch(function (err) {
    console.log(err);
})

//Longueur et Largeur de la zone du piano Roll
function resizeCanvasToDisplaySize(canvas) {
    // look up the size the canvas is being displayed
    var width = canvas.clientWidth;
    var height = canvas.clientHeight;

    // If it's resolution does not match change it
    if (canvas.width !== width || canvas.height !== height) {
        canvas.width = width;
        canvas.height = height;
        return true;
    }

    return false;
}

//Dessine le piano roll sans les touches ("le background")
function drawPianoGrid() {
    for (y = 0; y < w; y = y + cellheight) {
        for (x = 0; x < w; x = x + cellwidth) {
            if (x % 8 == 0) {
                ctx.beginPath();
                ctx.moveTo(x, 0);
                ctx.strokeStyle = "black";
                ctx.lineTo(x, h);
                ctx.shadowBlur = 0;
                ctx.stroke();
            }
            ctx.beginPath();
            if (y % 8) {
                ctx.fillStyle = "rgb(32,32,32)";
            } else {
                ctx.fillStyle = "rgb(40,40,40)";
            }
            ctx.strokeStyle = "rgb(24,24,24)";
            ctx.rect(x, y, cellwidth, cellheight);
            ctx.fill()
            ctx.stroke();
        }
    }
}

//Dessine les notes à chaque instant t jusqu'a la fin de l'intevale (80)
function drawNotes() {
    drawPianoGrid();
    var x = 0;
    for (var idx = intervDebut; idx < intervFin; idx++) {
        var y = 0;
        vectorPianoRoll[idx].forEach(function (e) {
            if (e != 0) {
                if (x == 1) { drawNote(x, y, 1); }
                else { drawNote(x, y, 1); }
            }
            y++;
        });
        x++;
    };
    drawPlayHead(60);
    intervDebut++;
    intervFin++;
}

//Dessine une note
function drawNote(x, y, length, selected = false) {
    x = x * cellwidth;
    y = y * cellheight;
    ctx.beginPath();
    ctx.fillStyle = "rgb(128,128,128)";
    if (selected) {
        ctx.strokeStyle = "rgb(255,255,255)";
    } else {
        ctx.strokeStyle = "rgb(24,24,24)";
    }
    ctx.rect(x, y, cellwidth * length, cellheight);
    ctx.fill()
    ctx.stroke();
}

//Dessine la barre rouge
function drawPlayHead(x) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineWidth = 2;
    ctx.strokeStyle = "red";
    ctx.lineTo(x, h);
    ctx.shadowBlur = 0;
    ctx.stroke();
}

