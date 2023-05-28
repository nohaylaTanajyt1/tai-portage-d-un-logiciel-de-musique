import mysql.connector
import config
import sys

sys.path.append('./src/backend/mysql/login')
from config import *

db = mysql.connector.connect(**connection_params)
