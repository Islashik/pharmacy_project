import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="medicine",
    db="chat",
    autocommit=True)
cursor = db.cursor()