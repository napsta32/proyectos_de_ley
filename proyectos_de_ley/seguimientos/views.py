# -*- encoding: utf-8 -*-
import re

from django.shortcuts import render

from . import utils


# Create your views here.
def index(request, short_url):
    short_url = re.sub("/seguimiento/", "", short_url)
    item = utils.get_proyecto_from_short_url(short_url)
    return render(request, "seguimientos/index.html", {"item": item})