import connexion
import utilisateurs as user
import mysql, sys, hashlib
sys.path.append('./src/backend/mysql/login')
from config import *

def getIdA(login):
    request = "SELECT id FROM Admin WHERE login = %s"
    params = [login]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)
#getId("mcjeangabin")

def getPassA(id):
    request = "SELECT password FROM Admin WHERE id = %s"
    params = [id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)
#getPass(1)

def getLoginA(id):
    request = "SELECT login FROM Admin WHERE id = %s"
    params = [id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)
#getLogin(1)

def getMailA(id):
    request = "SELECT mail FROM Admin WHERE id = %s"
    params = [id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)
#getMail(1)

def promoteAccountA(idU):
    request = "INSERT INTO Admin(id,login,password,mail) VALUES (%s,%s,%s,%s)"
    params = [idU,user.getLogin(idU),user.getPass(idU),user.getMail(idU)]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()
#promoteAccount(3)

def demoteAccountA(idA):
    request = "DELETE FROM Admin WHERE id = %s"
    params = [idA]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()
#demoteAccount("3")


def changeLoginA(id,login):
    request = "UPDATE Admin SET login = %s WHERE id = %s"
    params = [login,id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()
#changeLogin(3,"Jeanne")

def changePassA(id,password):
    request = "UPDATE Admin SET password = %s WHERE id = %s"
    params = [password,id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()
#changePass(3,"daa82c81b1efa758cb02a4639615bb2ad162013d4488e40512198b69f6e3a377")

def changeMailA(id,mail):
    request = "UPDATE Admin SET mail = %s WHERE id = %s"
    params = [mail,id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()
#changeMail(3,"jeanne@seriousmail.com")
