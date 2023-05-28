import connexion

def getIdArt(nom):
    request = "SELECT id FROM Artiste WHERE nom = %s"
    params = [nom]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)

def getAllArt(id):
    request = "SELECT nom, epoque, genre FROM Artiste WHERE id = %s"
    params = [id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)

def getNomArt(id):
    request = "SELECT nom FROM Artiste WHERE id = %s"
    params = [id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)

def getEpoqueArt(id):
    request = "SELECT epoque FROM Artiste WHERE id = %s"
    params = [id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)

def getGenreArt(id):
    request = "SELECT genre FROM Artiste WHERE id = %s"
    params = [id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)

def changeNomArt(id,nom):
    request = "UPDATE Artiste SET nom = %s WHERE id = %s"
    params = [nom,id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()

def changeEpoqueArt(id,epoque):
    request = "UPDATE Artiste SET epoque = %s WHERE id = %s"
    params = [epoque,id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()

def changeGenreArt(id,genre):
    request = "UPDATE Artiste SET genre = %s WHERE id = %s"
    params = [genre,id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()

def createArtisteArt(nom,epoque,genre):
    request = "INSERT INTO Artiste(nom,epoque,genre) VALUES (%s,%s,%s)"
    params = [nom,epoque,genre]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()

def deleteAccountArt(id):
    request = "DELETE FROM Artiste WHERE id = %s"
    params = [id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()