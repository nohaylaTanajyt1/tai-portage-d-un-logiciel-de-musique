import connexion, sys, mysql
sys.path.append('./src/backend/mysql/login')
from config import *

def verifLogin(login):
    request = "SELECT login FROM Users WHERE login = %s"
    params = login
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)


def verifPass(id):
    request = "SELECT password FROM Users WHERE id = %s"
    params = id
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(request, params)
            resultats = c.fetchall()
            for idL in resultats:
                return(idL)