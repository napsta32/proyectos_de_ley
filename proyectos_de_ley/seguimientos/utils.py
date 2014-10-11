from pdl.models import Proyecto


def get_proyecto_from_short_url(short_url):
    """
    :param short_url:
    :return: Proyecto model object
    """
    res = Proyecto.objects.get(short_url=short_url)
    print(short_url)
    return res

