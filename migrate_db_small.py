import dataset
import datetime
import os

"""Only migrate 100 records."""

old_db = os.path.join("..", "leyes.db")
new_db = "leyes_sqlite3.db"

db = dataset.connect("sqlite:///" + old_db)
res = db.query("select *  from proyectos")

new_items = []
j = 0
for i in res:
    timestamp = datetime.datetime.fromtimestamp(i['timestamp'])
    i['time_created'] = timestamp
    i['time_edited'] = timestamp

    try:
        fecha_presentacion = datetime.datetime.strptime(i['fecha_presentacion'],
                                                    '%d/%m/%Y')
    except ValueError:
        fecha_presentacion = datetime.datetime.strptime(i['fecha_presentacion'],
                                                        '%d/%m/%y')

    fecha_presentacion = datetime.datetime.date(fecha_presentacion)
    i['fecha_presentacion'] = fecha_presentacion

    i['expediente'] = i['link_to_pdf']

    if i['pdf_url'] is None:
        i['pdf_url'] = ''
    if i['seguimiento_page'] is None:
        i['seguimiento_page'] = ''

    del i['link_to_pdf']
    del i['timestamp']
    del i['id']
    del i['link']

    new_items.append(i)
    j += 1
    if j > 100:
        break

db = dataset.connect("sqlite:///" + new_db)
table = db['pdl_proyecto']
table.insert_many(new_items)
