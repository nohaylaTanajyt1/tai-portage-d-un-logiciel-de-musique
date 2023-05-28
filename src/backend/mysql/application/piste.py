import connexion

def getId(nom,idM, idI):
    request = "SELECT id FROM Piste WHERE nom = %s AND idM = %s AND idI = %s"
    params = [nom,idM, idI]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)

def getAll(id):
    request = "SELECT nom, idM, idI FROM Piste WHERE id = %s"
    params = [id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)

def getNom(id):
    request = "SELECT nom FROM Piste WHERE id = %s"
    params = [id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)

def getIdM(id):
    request = "SELECT idM FROM Piste WHERE id = %s"
    params = [id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)

def getIdI(id):
    request = "SELECT idI FROM Piste WHERE id = %s"
    params = [id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)

def changeNom(id,nom):
    request = "UPDATE Piste SET nom = %s WHERE id = %s"
    params = [nom,id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()

def changeIdM(id,idM):
    request = "UPDATE Piste SET idM = %s WHERE id = %s"
    params = [idM,id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()

def changeIdI(id,idI):
    request = "UPDATE Piste SET idI = %s WHERE id = %s"
    params = [idI,id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()

def createPiste(nom, idM, idI):
    request = "INSERT INTO Piste(nom, idM, idI) VALUES (%s,%s,%s)"
    params = [nom, tonalite, bpm, date_sortie, idA, genre]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()

def deletePiste(id):
    request = "DELETE FROM Piste WHERE id = %s"
    params = [id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()