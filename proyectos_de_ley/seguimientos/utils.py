import datetime
import unicodedata

from pdl.models import Proyecto
from pdl.models import Seguimientos
from pdl.models import Expedientes
from pdl.utils import convert_string_to_time


def get_proyecto_from_short_url(short_url):
    """
    :param short_url:
    :return: item for Proyecto
    """
    item = Proyecto.objects.get(short_url=short_url)
    if item.iniciativas_agrupadas is not None and \
            item.iniciativas_agrupadas != '' and '{' in \
            item.iniciativas_agrupadas:
        iniciativas = item.iniciativas_agrupadas.replace("{", "")
        iniciativas = iniciativas.replace("}", "")
        item.iniciativas_agrupadas = iniciativas.split(",")
    item.congresistas_with_links = hiperlink_congre(item.congresistas)
    item.fecha_presentacion = convert_string_to_time(item.fecha_presentacion)
    item.numero_congresistas = len(item.congresistas.split(","))
    return item


def get_events_from_expediente(id):
    """
    Uses the `proyecto_id` to obtain a list of events from the `expediente`
    page.

    :param id: proyecto_id as in table pdl_proyecto
    :return: list of events, which are key=>value dictionaries
    """
    events = Expedientes.objects.all().filter(proyecto=id).order_by('-fecha')
    return events


def get_seguimientos_from_proyecto_id(id):
    res = Seguimientos.objects.all().filter(proyecto_id=id)
    seguimientos = []
    append = seguimientos.append
    for i in res:
        obj = {}
        obj['startDate'] = str(i.fecha).replace("-", ",")
        obj['headline'] = i.evento
        append(obj)
    return seguimientos


def prepare_json_for_d3(item):
    if item.iniciativas_agrupadas is None:
        return {"nodes": ""}

    nodes = []
    append = nodes.append
    j = 1
    for i in item.iniciativas_agrupadas:
        queryset = Proyecto.objects.get(codigo=i)
        node = {"codigo": i, "url": "/p/" + queryset.short_url}
        append(node)
        j += 1

    # sort nodes by value (codigo)
    sorted_nodes_by_value = sorted(nodes, key=lambda k: k['codigo'])
    data_json = {"nodes": sorted_nodes_by_value}
    return data_json


def hiperlink_congre(congresistas):
    # tries to make a hiperlink for each congresista name to its own webpage
    if congresistas == '':
        return None

    for name in congresistas.split("; "):
        link = "<a href='/congresista/"
        link += str(convert_name_to_slug(name))
        link += "' title='ver todos sus proyectos'>"
        link += name + "</a>"
        congresistas = congresistas.replace(name, link)
    congresistas = congresistas.replace("; ", ";\n")
    return congresistas


def convert_name_to_slug(name):
    """Takes a congresista name and returns its slug."""
    name = name.strip()
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


def convert_date_to_string(dateobj):
    fecha = datetime.datetime.strftime(dateobj, '%Y-%m-%d')
    return fecha
