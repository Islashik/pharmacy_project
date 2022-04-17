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





cursor = db.cursor()


ointment = ointSQL(cursor=cursor)
syrup = syrupSQL(cursor=cursor)
syrups = syrup.extract_one_syrup(3)
# tablets_manager = tabletSQL(cursor=cursor)
# tablets = tablets_manager.extract_name()
print(syrups)



# for name, price, description in zip(tablets_name, tablets_price, tablets_description):
#     tablet.add_new_medicine(name, price, description)
#
# for name, price, description in zip(ointments_name, ointments_price, ointments_desc):
#     ointment.add_new_medicine(name, price, description)
#
# for name, price, description in zip(syrups_name, syrups_price, syrups_description):
#     syrup.add_new_medicine(name, price, description)