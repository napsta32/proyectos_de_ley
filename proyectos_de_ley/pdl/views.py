# -*- encoding: utf-8 -*-
import unicodedata

from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Q

from pdl.models import Proyecto


def index(request):
    items = get_last_items()
    return render(request, "pdl/index.html", {"items": items})


def proyecto(request, short_url):
    item = Proyecto.objects.get(short_url=short_url)
    num_proy = item.numero_proyecto
    item = prettify_item(item)
    return render(request, "pdl/proyecto.html", {'item': item, 'num_proy':
                                                 num_proy,
                                                 }
                  )


def about(request):
    return render(request, "pdl/about.html")


def search(request):
    if 'q' in request.GET:
        query = request.GET['q']
        query = sanitize(query)
        if query.strip() == '':
            return redirect("/")
        else:
            results = find_in_db(query)
        return render(request, "pdl/search.html", {"results": results,
                                                   "keyword": query})
    return redirect("/")


def congresista(request, congresista_slug):
    results = find_slug_in_db(congresista_slug.replace('/', ''))
    return render(request, "pdl/congresista.html", {"results":
                                                        results, "congresista":
                                                        congresista_slug})


def find_in_db(query):
    items = Proyecto.objects.filter(
        Q(short_url__icontains=query) |
        Q(codigo__icontains=query) |
        Q(numero_proyecto__icontains=query) |
        Q(titulo__icontains=query) |
        Q(pdf_url__icontains=query) |
        Q(expediente__icontains=query) |
        Q(seguimiento_page__icontains=query) |
        Q(congresistas__icontains=query),
    ).order_by('-codigo')
    if len(items) > 0:
        results = []
        for i in items:
            results.append(prettify_item_small(i))
    else:
        results = "No se encontraron resultados."
    return results


def find_slug_in_db(query):
    items = Proyecto.objects.filter(
        Q(congresistas_slug__icontains=query),
        ).order_by('-codigo')
    if len(items) > 0:
        results = []
        for i in items:
            results.append(prettify_item(i))
    else:
        results = "No se encontraron resultados."
    return results


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
    items = Proyecto.objects.all().order_by('-codigo')
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
        out += " href='" + item.pdf_url + "' role='button'>PDF</a>\n"
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
        out += " href='" + item.seguimiento_page
        out += "' role='button'>Seguimiento</a>"
    return out


def prettify_item_small(item):
    out = "<p><a href='/p/" + item.short_url
    out += "' title='Permalink'>"
    out += item.codigo
    out += "</a>\n "
    out += item.titulo
    if item.pdf_url != '':
        out += '\n <span class="glyphicon glyphicon-cloud-download"></span>'
        out += ' <a href="' + item.pdf_url + '">PDF</a>'
    else:
        out += ' [sin PDF]'

    if item.expediente != '':
        out += '\n <span class="glyphicon glyphicon-link"></span>'
        out += ' <a href="' + item.expediente + '">Expediente</a>'
    else:
        out += ' [sin Expediente]'

    if item.seguimiento_page != '':
        out += '\n <span class="glyphicon glyphicon-link"></span>'
        out += ' <a href="' + item.seguimiento_page + '">Seguimiento</a>'
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
