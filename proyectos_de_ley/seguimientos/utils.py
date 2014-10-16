from pdl.models import Proyecto


def get_proyecto_from_short_url(short_url):
    """
    :param short_url:
    :return: Proyecto model object
    """
    item = Proyecto.objects.get(short_url=short_url)
    if item.iniciativas_agrupadas is not None and '{' in \
            item.iniciativas_agrupadas:
        iniciativas = item.iniciativas_agrupadas.replace("{", "")
        iniciativas = iniciativas.replace("}", "")
        item.iniciativas_agrupadas = iniciativas.split(",")
    return item


def prepare_json_for_d3(item):
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


