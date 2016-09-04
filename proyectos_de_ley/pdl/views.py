# -*- encoding: utf-8 -*-
import re

from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from .utils import prettify_item
from .utils import do_pagination
from .utils import find_slug_in_db
from pdl.models import Proyecto
from pdl.forms import SimpleSearchForm
from stats.models import Dispensed


def index(request):
    all_items = Proyecto.objects.filter(legislatura=2016).order_by('-codigo')
    obj = do_pagination(request, all_items)

    # sin fusionar
    numero_de_proyectos = len(all_items)
    with_iniciativas = Proyecto.objects.filter(legislatura=2016).exclude(
        iniciativas_agrupadas__isnull=True).exclude(
        iniciativas_agrupadas__exact='').count()
    without_iniciativas = numero_de_proyectos - with_iniciativas

    # no son ley
    projects_empty_title = Proyecto.objects.filter(
        titulo_de_ley='',
        legislatura=2016,
    ).count()
    projects_null_title = Proyecto.objects.filter(
        titulo_de_ley__isnull=True,
        legislatura=2016,
    ).count()
    are_not_law = projects_empty_title + projects_null_title

    # total aprobados
    try:
        res = Dispensed.objects.all()[0]
        aprobados = res.total_approved
    except IndexError:
        aprobados = 0

    return render(request, "pdl/index.html", {
        "items": obj['items'],
        "pretty_items": obj['pretty_items'],
        "first_half": obj['first_half'],
        "second_half": obj['second_half'],
        "first_page": obj['first_page'],
        "last_page": obj['last_page'],
        "current": obj['current'],
        # stats
        "total": numero_de_proyectos,
        "sin_fusionar": without_iniciativas,
        "no_son_ley": are_not_law,
        "aprobados": aprobados,
    })


def proyecto(request, short_url):
    try:
        item = Proyecto.objects.get(short_url=short_url)
        num_proy = item.numero_proyecto
        item = prettify_item(item)
        return render(request, "pdl/proyecto.html", {'item': item, 'num_proy':
                                                     num_proy,
                                                     }
                      )
    except Proyecto.DoesNotExist:
        msg = [
            "No se pudo encontrar el proyecto.",
            "Quizá ingresó URL incorrecto."
        ]
        return render(request, "pdl/proyecto.html", {"msg": msg})


def about(request):
    return render(request, "pdl/about.html")


@csrf_exempt
def search(request):
    if 'q' not in request.GET:
        return redirect('/')

    query = request.GET['q']
    if query.strip() == '':
        return redirect('/')

    form = SimpleSearchForm(request.GET)
    all_items = form.search()
    obj = do_pagination(request, all_items, search=True)

    keywords = clean_my_query(query)

    return render(request, "pdl/search.html", {
        "result_count": len(all_items),
        "items": obj['items'],
        "pretty_items": obj['pretty_items'],
        "first_half": obj['first_half'],
        "second_half": obj['second_half'],
        "first_page": obj['first_page'],
        "last_page": obj['last_page'],
        "current": obj['current'],
        "keywords": keywords,
        "query": query,
        "pagination_keyword": query,
    })


def clean_my_query(query):
    keywords = re.sub('\s+', ' ', query)
    keywords = re.sub('\s+$', '', keywords)
    keywords = re.sub('^\s+', '', keywords)
    keywords = keywords.split(' ')
    return keywords


def congresista(request, congresista_slug):
    if congresista_slug.strip() == '':
        return redirect('/')

    congresista_name = find_slug_in_db(congresista_slug)
    if congresista_name is not None:
        all_items = Proyecto.objects.filter(
            congresistas__icontains=congresista_name).order_by('-codigo')
        obj = do_pagination(request, all_items)
        return render(request, "pdl/congresista.html", {
            "items": obj['items'],
            "pretty_items": obj['pretty_items'],
            "first_half": obj['first_half'],
            "second_half": obj['second_half'],
            "first_page": obj['first_page'],
            "last_page": obj['last_page'],
            "current": obj['current'],
            "congresista": congresista_name,
            "slug": congresista_slug.replace("/", ""),
        })
    else:
        msg = [
            "No se pudo encontrar el congresista.",
            "Quizá el nombre está incorrecto."
        ]
        return render(request, "pdl/congresista.html", {"msg": msg})
