from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from pdl.models import Proyecto
from .serializers import ProyectoSerializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def proyecto(request, numero):
    """
    Lista metadatos de cada proyecto de ley.
    """
    try:
        proy = Proyecto.objects.get(codigo=numero)
    except Proyecto.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ProyectoSerializer(proy)
        return JSONResponse(serializer.data)
