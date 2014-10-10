# -*- encoding: utf-8 -*-
from django.shortcuts import render


# Create your views here.
def index(request, short_url):
    return render(request, "pdl/index.html", {"msg": short_url})