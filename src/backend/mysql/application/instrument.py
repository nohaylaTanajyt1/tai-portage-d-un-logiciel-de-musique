import connexion

def getIdInst(nom, logo):
    request = "SELECT id FROM Instrument WHERE nom = %s AND logo = %s"
    params = [nom, logo]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)

def getAllInst(id):
    request = "SELECT nom, logo FROM Instrument WHERE id = %s"
    params = [id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)

def getNomInst(id):
    request = "SELECT nom FROM Instrument WHERE id = %s"
    params = [id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)

def getNomInst(id):
    request = "SELECT logo FROM Instrument WHERE id = %s"
    params = [id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)

def changeNomInst(id,nom):
    request = "UPDATE Instrument SET nom = %s WHERE id = %s"
    params = [nom,id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()

def changeLogoInst(id,logo):
    request = "UPDATE Instrument SET logo = %s WHERE id = %s"
    params = [logo,id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()

def createInstrumentInst(nom, logo):
    request = "INSERT INTO Instrument(nom, logo) VALUES (%s,%s)"
    params = [nom, logo]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()

def deleteInstrumentInst(id):
    request = "DELETE FROM Instrument WHERE id = %s"
    params = [id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()