import connexion
import mysql, sys, hashlib
sys.path.append('./src/backend/mysql/login')
from config import *

def getId(login):
    request = "SELECT id FROM Users WHERE login = %s"
    params = [login]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)
#getId("mcjeangabin")

def getPass(id):
    request = "SELECT password FROM Users WHERE id = %s"
    params = [id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)
#getPass(1)

def getLogin(id):
    request = "SELECT login FROM Users WHERE id = %s"
    params = [id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)
#getLogin(1)

def getMail(id):
    request = "SELECT mail FROM Users WHERE id = %s"
    params = [id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)
#getMail(1)

def createAccount(login,password,mail):
    request = "INSERT INTO Users(login,password,mail) VALUES (%s,%s,%s)"
    params = [login,password,mail]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()
#createAccount("Jeanne","55f2522075c2894589a83163f38477a1c0c6f891eab7ce840b4dfe47a790b6ee","jeannebutebeacoup@coolmail.fr")

def deleteAccount(id):
    request = "DELETE FROM Users WHERE id = %s"
    params = [id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()
#deleteAccount("2")


def changeLogin(id,login):
    request = "UPDATE Users SET login = %s WHERE id = %s"
    params = [login,id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()
#changeLogin(3,"Jeanne")

def changePass(id,password):
    request = "UPDATE Users SET password = %s WHERE id = %s"
    params = [password,id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()
#changePass(3,"daa82c81b1efa758cb02a4639615bb2ad162013d4488e40512198b69f6e3a377")

def changeMail(id,mail):
    request = "UPDATE Users SET mail = %s WHERE id = %s"
    params = [mail,id]
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            db.commit()
#changeMail(3,"jeanne@seriousmail.com")
