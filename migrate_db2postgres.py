import dataset
import datetime
import os
import unicodedata
import sys


#old_db_path = os.path.join("proyectos_de_ley", "leyes_sqlite3.db")
old_db_path = os.path.join("leyes_sqlite3.db")
new_db = dataset.connect("postgresql://proyectosdeley:PASSWORD@localhost:5432/pdl")

old_db = dataset.connect("sqlite:///" + old_db_path)

res = old_db.query("select *  from pdl_proyecto")
table = new_db['pdl_proyecto']
table.insert_many(res)


res = old_db.query("select *  from pdl_slug")
table = new_db['pdl_slug']
table.insert_many(res)

res = old_db.query("select *  from pdl_seguimientos")
table = new_db['pdl_seguimientos']
table.insert_many(res)

