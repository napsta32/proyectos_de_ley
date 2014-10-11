# -*- encoding: utf-8 -*-
from django.shortcuts import render


# Create your views here.
def index(request, short_url):
    return render(request, "seguimientos/index.html", {"msg": short_url})