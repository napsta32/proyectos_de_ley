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

