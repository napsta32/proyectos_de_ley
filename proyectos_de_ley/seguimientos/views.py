# -*- encoding: utf-8 -*-
import re

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets

from . import utils
from pdl.models import Proyecto
from .serializers import IniciativasSerializer


# Create your views here.
def index(request, short_url):
    short_url = re.sub("/seguimiento/", "", short_url)
    item = utils.get_proyecto_from_short_url(short_url)
    return render(request, "seguimientos/index.html", {"item": item})

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def iniciativa_list(request, short_url):
    """List all iniciativas for proyecto."""
    try:
        item = utils.get_proyecto_from_short_url(short_url=short_url)
        new_item = utils.prepare_json_for_d3(item)
    except Proyecto.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = IniciativasSerializer(new_item)
        print(serializer.data)
        return JSONResponse(serializer.data)
