import dataset
import datetime
import os
import unicodedata


"""Only migrate 100 records."""
def convert_name_to_slug(name):
    """Takes a congresista name and returns its slug."""
    name = name.replace(",", "").lower()
    name = name.split(" ")

    if len(name) > 2:
        i = 0
        slug = ""
        while i < 3:
            slug += name[i]
            if i < 2:
                slug += "_"
            i += 1
        slug = unicodedata.normalize('NFKD', slug).encode('ascii', 'ignore')
        slug = str(slug, encoding="utf-8")
        return slug + "/"

old_db = os.path.join("..", "leyes.db")
new_db = "leyes_sqlite3.db"

db = dataset.connect("sqlite:///" + old_db)
res = db.query("select *  from proyectos")

new_items = []
slugs = []  # translation table between name an URL
j = 0
for i in res:
    timestamp = datetime.datetime.fromtimestamp(i['timestamp'])
    i['time_created'] = timestamp
    i['time_edited'] = timestamp

    try:
        fecha_presentacion = datetime.datetime.strptime(
            i['fecha_presentacion'],
            '%d/%m/%Y',
        )
    except ValueError:
        fecha_presentacion = datetime.datetime.strptime(
            i['fecha_presentacion'],
            '%d/%m/%y',
        )

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

    congresistas = i['congresistas'].split(';')
    for congre in congresistas:
        congre = congre.strip()
        obj = dict(nombre=congre)
        if congre is not None and congre.strip() != '':
            congre_slug = convert_name_to_slug(congre)
            obj['slug'] = congre_slug
            if obj not in slugs:
                slugs.append(obj)

    new_items.append(i)
    j += 1
    if j > 100:
        break

db = dataset.connect("sqlite:///" + new_db)
table = db['pdl_proyecto']
table.insert_many(new_items)

table = db['pdl_slug']
print(len(slugs))
table.insert_many(slugs)
