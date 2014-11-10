# -*- encoding: utf-8 -*-
from functools import reduce
import unicodedata

from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from pdl.models import Proyecto
from pdl.models import Slug
from pdl.utils import Timer


def index(request):
    all_items = Proyecto.objects.all().order_by('-codigo')
    obj = do_pagination(request, all_items)

    return render(request, "pdl/index.html", {
        "items": obj['items'],
        "pretty_items": obj['pretty_items'],
        "first_half": obj['first_half'],
        "second_half": obj['second_half'],
        "first_page": obj['first_page'],
        "last_page": obj['last_page'],
        "current": obj['current'],
        }
    )


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


def search(request):
    # TODO: include seguimientos in search fields so that input can be Ley
    # Number and output the proyecto that originated such law.
    if 'q' in request.GET:
        query = request.GET['q']
        query = sanitize(query)
        if query.strip() == '':
            return redirect("/")
        else:
            results = find_in_db(query)

        if results == "No se encontraron resultados.":
            return render(request, "pdl/search.html", {"results": results,
                                                       "keyword": query})
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
                "keyword": query,
                }
            )
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
            }
        )
    else:
        msg = [
            "No se pudo encontrar el congresista.",
            "Quizá el nombre está incorrecto."
        ]
        return render(request, "pdl/congresista.html", {"msg": msg})


def do_pagination(request, all_items, search=False):
    """
    :param request: contains the current page requested by user
    :param all_items:
    :param search: if search is False items will be prettified in long form.
           if search is True then items will be prettified as small items
           for search results.
    :return: dict containing paginated items and pagination bar
    """
    if search is False:
        paginator = Paginator(all_items, 20)
    else:
        paginator = Paginator(all_items, 40)

    page = request.GET.get('page')

    try:
        items = paginator.page(page)
        cur = int(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        items = paginator.page(1)
        cur = 1
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        items = paginator.page(paginator.num_pages)
        cur = 1

    pretty_items = []
    for i in items.object_list:
        if search is False:
            pretty_items.append(prettify_item(i))
        else:
            pretty_items.append(prettify_item_small(i))

    if cur > 20:
        first_half = range(cur - 10, cur)
        # is current less than last page?
        if cur < paginator.page_range[-1] - 10:
            second_half = range(cur + 1, cur + 10)
        else:
            second_half = range(cur + 1, paginator.page_range[-1])
    else:
        first_half = range(1, cur)
        if paginator.page_range[-1] > 20:
            second_half = range(cur + 1, 21)
        else:
            second_half = range(cur + 1, paginator.page_range[-1] + 1)

    obj = {
        'items': items,
        "pretty_items": pretty_items,
        "first_half": first_half,
        "second_half": second_half,
        "first_page": paginator.page_range[0],
        "last_page": paginator.page_range[-1],
        "current": cur,
        }
    return obj


def find_in_db(query):
    """
    Finds items according to user search.

    :param query: user's keyword
    :return: QuerySet object with items or string if no results were found.
    """
    keywords = query.split(" ")
    with Timer() as t:
        items = Proyecto.objects.filter(
            reduce(lambda x, y: x | y, [Q(short_url__icontains=word) for word in keywords]) |
            reduce(lambda x, y: x | y, [Q(codigo__icontains=word) for word in keywords]) |
            reduce(lambda x, y: x | y, [Q(numero_proyecto__icontains=word) for word in keywords]) |
            reduce(lambda x, y: x | y, [Q(titulo__icontains=word) for word in keywords]) |
            reduce(lambda x, y: x | y, [Q(expediente__icontains=word) for word in keywords]) |
            reduce(lambda x, y: x | y, [Q(congresistas__icontains=word) for word in keywords]),
            # Q(pdf_url__icontains=query) |
            # Q(seguimiento_page__icontains=query),
        ).order_by('-codigo')
    print("=> elasped lpop: %s s" % t.secs)
    if len(items) > 0:
        results = items
    else:
        results = "No se encontraron resultados."
    return results


def find_slug_in_db(congresista_slug):
    try:
        item = Slug.objects.get(slug=congresista_slug)
        return item.nombre
    except Slug.DoesNotExist:
        try:
            congresista_slug += '/'
            item = Slug.objects.get(slug=congresista_slug)
            return item.nombre
        except Slug.DoesNotExist:
            return None


def sanitize(s):
    s = s.replace("'", "")
    s = s.replace('"', "")
    s = s.replace("/", "")
    s = s.replace("\\", "")
    s = s.replace(";", "")
    s = s.replace("=", "")
    s = s.replace("*", "")
    s = s.replace("%", "")
    return s


def get_last_items():
    """All items from the database are extracted as list of dictionaries."""
    items = Proyecto.objects.all().order_by('-codigo')[:20]
    pretty_items = []
    for i in items:
        pretty_items.append(prettify_item(i))
    return pretty_items


def prettify_item(item):
    out = "<p>"
    out += "<a href='/p/" + str(item.short_url)
    out += "' title='Permalink'>"
    out += "<b>" + item.numero_proyecto + "</b></a></p>\n"
    out += "<h4>" + item.titulo + "</h4>\n"
    out += "<p>" + hiperlink_congre(item.congresistas) + "</p>\n"

    if item.pdf_url != '':
        out += "<a class='btn btn-lg btn-primary'"
        out += " href='" + str(item.pdf_url) + "' role='button'>PDF</a>\n"
    else:
        out += "<a class='btn btn-lg btn-primary disabled'"
        out += " href='#' role='button'>Sin PDF</a>\n"

    if item.expediente != '':
        out += "<a class='btn btn-lg btn-primary'"
        out += " href='" + item.expediente
        out += "' role='button'>EXPEDIENTE</a>\n"
    else:
        out += "<a class='btn btn-lg btn-primary disabled'"
        out += " href='#' role='button'>Sin EXPEDIENTE</a>\n"

    if item.seguimiento_page != '':
        out += "<a class='btn btn-lg btn-primary'"
        out += " href='/p/" + item.short_url + "/seguimiento"
        out += "' role='button'>Seguimiento</a>"
    return out


def prettify_item_small(item):
    out = "<p><a href='/p/" + item.short_url
    out += "' title='Permalink'>"
    out += item.codigo
    out += "</a>\n "
    out += item.titulo
    if item.pdf_url != '' and item.pdf_url is not None:
        out += '\n <span class="glyphicon glyphicon-cloud-download"></span>'
        out += ' <a href="' + item.pdf_url + '">PDF</a>'
    else:
        out += ' [sin PDF]'

    if item.expediente != '' and item.expediente is not None:
        out += '\n <span class="glyphicon glyphicon-link"></span>'
        out += ' <a href="' + item.expediente + '">Expediente</a>'
    else:
        out += ' [sin Expediente]'

    if item.seguimiento_page != '' and item.seguimiento_page is not None:
        out += '\n <span class="glyphicon glyphicon-link"></span>'
        out += ' <a href="/p/' + item.short_url + \
               '/seguimiento">Seguimiento</a>'
    else:
        out += '\n [sin Seguimiento]'
    out += '</p>'
    return out


def hiperlink_congre(congresistas):
    # tries to make a hiperlink for each congresista name to its own webpage
    for name in congresistas.split("; "):
        link = "<a href='/congresista/"
        link += str(convert_name_to_slug(name))
        link += "' title='ver todos sus proyectos'>"
        link += name + "</a>"
        congresistas = congresistas.replace(name, link)
    congresistas = congresistas.replace("; ", ";\n")
    return congresistas


def convert_name_to_slug(name):
    """Takes a congresista name and returns its slug."""
    name = name.strip()
    name = name.replace(",", "").lower()
    name = name.split(" ")

    if len(name) > 2:
        i = 0
        slug = ""
        while i < 3:
            slug += name[i]
            if i < 2:
                slug += "_"
            i += 1
        slug = unicodedata.normalize('NFKD', slug).encode('ascii', 'ignore')
        slug = str(slug, encoding="utf-8")
        return slug + "/"
