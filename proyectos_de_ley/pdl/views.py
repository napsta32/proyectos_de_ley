from django.shortcuts import render

from pdl.models import Proyecto


def index(request):
    items = ["hola", "que", "ase"]
    return render(request, "pdl/index.html", {"items": items})

def get_last_items():
    items = Proyecto.objects.all().order_by('-codigo')
    return items
