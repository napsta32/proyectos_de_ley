from pdl.models import Proyecto


def get_proyecto_from_short_url(short_url):
    """
    :param short_url:
    :return: Proyecto model object
    """
    item = Proyecto.objects.get(short_url=short_url)
    if '{' in item.iniciativas_agrupadas:
        iniciativas = item.iniciativas_agrupadas.replace("{", "")
        iniciativas = iniciativas.replace("}", "")
        item.iniciativas_agrupadas = iniciativas.split(",")
    return item

def prepare_json_for_d3(item):
    nodes = [{"name": item.codigo, "url": "/p/"}]
    append = nodes.append
    j = 1
    for i in item.iniciativas_agrupadas:
        node = {"name": i, "url": "/p/" + i}
        append(node)
        j += 1

    links = []
    append = links.append
    j = 1
    for i in item.iniciativas_agrupadas:
        link = {"source": j, "target": 0, "value": 1}
        append(link)
        j += 1

    data_json = {"nodes": nodes, "links": links}
    return data_json


