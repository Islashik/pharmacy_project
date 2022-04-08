import mysql.connector
from sql.tablets_sql import tabletSQL
from sql.ointments_sql import ointSQL
from sql.syrups_sql import syrupSQL
from data.syrups import syrups_name,syrups_price,syrups_description
from data.ointments import ointments_name,ointments_price,ointments_desc
from data.tablets import tablets_price, tablets_name, tablets_description
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Abc12345!",
    db="Neman",
    autocommit=True)
print('connected')




cursor = db.cursor()

tablet = tabletSQL(cursor=cursor)
ointment = ointSQL(cursor=cursor)
syrup = syrupSQL(cursor=cursor)



for name, price, description in zip(tablets_name, tablets_price, tablets_description):
    tablet.add_new_medicine(name, price, description)

for name, price, description in zip(ointments_name, ointments_price, ointments_desc):
    ointment.add_new_medicine(name, price, description)

for name, price, description in zip(syrups_name, syrups_price, syrups_description):
    syrup.add_new_medicine(name, price, description)