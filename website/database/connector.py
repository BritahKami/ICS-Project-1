import mysql.connector
from ..config import env

#Establishing SQL Connection
def dbconnector():
    return mysql.connector.connect(
        host=env.DB_HOST,
        user=env.DB_USER,
        password=env.DB_PASS,
        database=env.DB_NAME
    )