# -*- encoding: utf-8 -*-
import re

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer

from pdl.models import Proyecto
from . import utils
from .serializers import IniciativasSerializer, SeguimientosSerializer


# Create your views here.
def index(request, short_url):
    short_url = re.sub("/seguimiento/", "", short_url)
    item = utils.get_proyecto_from_short_url(short_url)
    item.expediente_events = utils.get_events_from_expediente(item.id)
    return render(request, "seguimientos/index.html", {"item": item})


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny, ))
def iniciativa_list(request, short_url):
    """Lista todas las iniciativas que se agruparon para proyecto de ley.
    ---
    type:
      short_url:
        required: true
        type: string


    parameters:
      - name: short_url
        description: URL que identifica cada proyecto de ley, por ejemplo 4skzgv
        type: string
        paramType: path
    """
    try:
        item = utils.get_proyecto_from_short_url(short_url=short_url)
        new_item = utils.prepare_json_for_d3(item)
    except Proyecto.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = IniciativasSerializer(new_item)
        return JSONResponse(serializer.data)


class MyObj(object):
    pass


@csrf_exempt
def seguimientos_list(request, short_url):
    """List all seguimientos for proyecto."""
    try:
        item = utils.get_proyecto_from_short_url(short_url=short_url)
        seguimientos = utils.get_seguimientos_from_proyecto_id(item.id)
        seguimientos.append({
            'headline': 'Fecha de presentación',
            'startDate': utils.convert_date_to_string(item.fecha_presentacion).replace("-", ","),
        })
        obj = MyObj()

        mydict = {}
        mydict['type'] = 'default'
        mydict['text'] = "Proyecto No: " + str(item.numero_proyecto).replace("/", "_")
        mydict['date'] = seguimientos

        obj.timeline = mydict
    except Proyecto.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SeguimientosSerializer(obj)
        return JSONResponse(serializer.data)
