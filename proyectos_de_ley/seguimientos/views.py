# -*- encoding: utf-8 -*-
import re

from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets

from . import utils
from pdl.models import Proyecto
from .serializers import UserSerializer


# Create your views here.
def index(request, short_url):
    short_url = re.sub("/seguimiento/", "", short_url)
    item = utils.get_proyecto_from_short_url(short_url)
    return render(request, "seguimientos/index.html", {"item": item})

class UserViewSet(viewsets.ModelViewSet):
    """
    Returns JSON object of iniciativas as required by AJAX get.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer