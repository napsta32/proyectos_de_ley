# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from pdl.models import Proyecto
from .utils import prettify_item
from .utils import sanitize
from .utils import find_in_db
from .utils import do_pagination
from .utils import find_slug_in_db
from stats.models import Dispensed


def index(request):
    all_items = Proyecto.objects.all().order_by('-codigo')
    obj = do_pagination(request, all_items)

    # sin fusionar
    numero_de_proyectos = len(all_items)
    with_iniciativas = Proyecto.objects.exclude(
        iniciativas_agrupadas__isnull=True).exclude(
        iniciativas_agrupadas__exact='').count()
    without_iniciativas = numero_de_proyectos - with_iniciativas

    # no son ley
    are_law = Proyecto.objects.exclude(
        titulo_de_ley__isnull=True).exclude(
        titulo_de_ley__exact='').count()
    are_not_law = numero_de_proyectos - are_law

    # total aprobados
    res = Dispensed.objects.all()[0]
    aprobados = res.total_approved

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
    if 'q' in request.GET:
        query = request.GET['q']
        query = sanitize(query)
        if query.strip() == '':
            return redirect("/")
        else:
            results = find_in_db(query)

        if results == "No se encontraron resultados.":
            return render(request, "pdl/search.html", {"results": results,
                                                       "query": query})
        else:
            all_items = results
            obj = do_pagination(request, all_items, search=True)
            return render(request, "pdl/search.html", {
                "items": obj['items'],
                "pretty_items": obj['pretty_items'],
                "first_half": obj['first_half'],
                "second_half": obj['second_half'],
                "first_page": obj['first_page'],
                "last_page": obj['last_page'],
                "current": obj['current'],
                "keywords": query.split(" "),
                "query": query,
                "pagination_keyword": query,
            })
    return redirect("/")


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
