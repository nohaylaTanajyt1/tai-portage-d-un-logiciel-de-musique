import connexion

def getIdM(nom,idA):
    request = "SELECT id FROM Morceau WHERE nom = %s AND idA = %s"
    params = [nom,idA]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)

def getAllM(id):
    request = "SELECT nom, tonalite, bpm, date_sortie, idA, genre FROM Morceau WHERE id = %s"
    params = [id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)

def getAllM(nom, idA):
    request = "SELECT nom, tonalite, bpm, date_sortie, idA, genre FROM Morceau WHERE nom = %s AND idA = %s"
    params = [nom, idA]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)

def getNomM(id):
    request = "SELECT nom FROM Morceau WHERE id = %s"
    params = [id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)

def getTonaliteM(id):
    request = "SELECT tonalite FROM Morceau WHERE id = %s"
    params = [id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)

def getBpmM(id):
    request = "SELECT bpm FROM Morceau WHERE id = %s"
    params = [id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)

def getDate_sortieM(id):
    request = "SELECT date_sortie FROM Morceau WHERE id = %s"
    params = [id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)

def getIdAM(id):
    request = "SELECT idA FROM Morceau WHERE id = %s"
    params = [id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)
"""         
def getDescriptionM(id):
    request = "SELECT description FROM Morceau WHERE id = %s"
    params = [id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)
"""
def changeNomM(id,nom):
    request = "UPDATE Morceau SET nom = %s WHERE id = %s"
    params = [nom,id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()

def changeTonaliteM(id,tonalite):
    request = "UPDATE Morceau SET tonalite = %s WHERE id = %s"
    params = [tonalite,id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()

def changeBpmM(id,bpm):
    request = "UPDATE Morceau SET bpm = %s WHERE id = %s"
    params = [bpm,id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()

def changeDate_SortieM(id,date_sortie):
    request = "UPDATE Morceau SET date_sortie = %s WHERE id = %s"
    params = [date_sortie,id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()

def changeIdAM(id,ida):
    request = "UPDATE Morceau SET idA = %s WHERE id = %s"
    params = [ida,id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()

def changeGenreM(id,genre):
    request = "UPDATE Morceau SET genre = %s WHERE id = %s"
    params = [genre,id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()
"""
def changeDescriptionM(id,description):
    request = "UPDATE Morceau SET description = %s WHERE id = %s"
    params = [description,id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()
"""
def createMorceauM(nom, tonalite, bpm, date_sortie, idA, genre):
    request = "INSERT INTO Morceau(nom, tonalite, bpm, date_sortie, idA, genre) VALUES (%s,%s,%s,%s,%s,%s)"
    params = [nom, tonalite, bpm, date_sortie, idA, genre]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()

def deleteMorceauM(id):
    request = "DELETE FROM Morceau WHERE id = %s"
    params = [id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()
