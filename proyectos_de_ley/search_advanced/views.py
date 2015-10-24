# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.db.models import Q

from . import forms
from pdl.models import Proyecto
from pdl.models import Seguimientos
from pdl.utils import do_pagination


def index(request):
    if request.method == 'GET':
        form = forms.SearchAdvancedForm(request.GET)
        if form.is_valid():
            keywords = clean_keywords_for_combined_search(form.cleaned_data)
            if len(keywords) > 0:
                return combined_search(keywords, form, request)

            # requests from stats view
            if form.cleaned_data['dictamen'] == 'NÚMERO TOTAL DE LEYES':
                return search_total_leyes(form, request)

            if form.cleaned_data['dictamen'] == 'Exonerados de dictamen':
                return search_exonerados_dictamen(form, request)

            if form.cleaned_data['dispensados_2da_votacion'] == 'TOTAL dispensados':
                return search_dispensados_todos(form, request)

            if form.cleaned_data['dispensados_2da_votacion'] == 'TOTAL aprobados':
                return search_total_aprobados(form, request)

            if form.cleaned_data['dispensados_2da_votacion'] == 'Dispensados por acuerdo del pleno':
                return search_dispensados_acuerdo_pleno(form, request)

            if form.cleaned_data['dispensados_2da_votacion'] == 'Dispensados por junta portavoces':
                return search_dispensados_junta_portavoces(form, request)

            if form.cleaned_data['dispensados_2da_votacion'] == 'Otros proyectos dispensados':
                return search_dispensados_otros(form, request)

            return render(request, "search_advanced/index.html", {
                "form": form,
            })
        else:
            print(form.errors)
            return render(request, "search_advanced/index.html", {
                "form": form,
            })


def clean_keywords_for_combined_search(cleaned_data):
    keywords = {}
    for k, v in cleaned_data.items():
        if v != '' and v is not None:
            if v in ['---', '--Escoger bancada--']:
                continue
            if k in ['dispensados_2da_votacion', 'dictamen']:
                continue
            keywords[k] = v
    return keywords


def combined_search(keywords, form, request):
    msg = ''
    queryset = Proyecto.objects.all().order_by('-codigo')
    if 'query' in keywords:
        msg = "Número de proyectos encontrados"
        queryset = queryset.filter(titulo__icontains=keywords['query'])
    if 'date_to' and 'date_from' in keywords:
        msg = "Número de proyectos entre fecha indicada"
        queryset = queryset.filter(fecha_presentacion__range=(keywords['date_from'], keywords['date_to']))
    if 'congresista' in keywords:
        msg = "Número de proyectos de congresista {}".format(keywords['congresista'])
        queryset = queryset.filter(congresistas__icontains=keywords['congresista'])
    if 'grupo_parlamentario' in keywords:
        msg = "Número de proyectos de bancada {}".format(keywords['grupo_parlamentario'])
        queryset = queryset.filter(grupo_parlamentario=keywords['grupo_parlamentario'])
    if 'comision' in keywords:
        msg = "Número de proyectos de comisión {}".format(keywords['comision'])
        queryset = filter_by_comision(keywords, queryset)

    if len(keywords) > 1:
        msg = "Número de proyectos encontrados"

    if queryset:
        obj = do_pagination(request, queryset, search=True, advanced_search=True)
        return render(request, "search_advanced/index.html", {
            "query": keywords['query'],
            "result_count": len(queryset),
            "extra_result_msg": msg,
            "items": obj['items'],
            "pretty_items": obj['pretty_items'],
            "first_half": obj['first_half'],
            "second_half": obj['second_half'],
            "first_page": obj['first_page'],
            "last_page": obj['last_page'],
            "current": obj['current'],
            "form": form,
        })
    else:
        return render(request, "search_advanced/index.html", {
            "form": form,
            "info_msg": 'No se encontraron resultados para esa combinación de términos de búsqueda',
        })


def filter_by_comision(keywords, queryset):
    commission = keywords['comision']
    return queryset.filter(projectsincommissions__commission=commission)


def search_dispensados_todos(form, request):
    total_dispensed = [i.proyecto for i in Seguimientos.objects.select_related('proyecto').filter(
                       evento__icontains='dispensado 2da')]

    obj = do_pagination(request, total_dispensed, search=True, advanced_search=True)
    return render(request, "search_advanced/index.html", {
        "result_count": len(total_dispensed),
        "extra_result_msg": "Total número de proyectos dispensados de 2da votación",
        "items": obj['items'],
        "pretty_items": obj['pretty_items'],
        "first_half": obj['first_half'],
        "second_half": obj['second_half'],
        "first_page": obj['first_page'],
        "last_page": obj['last_page'],
        "current": obj['current'],
        "form": form,
        "comision": obj['comision'],
    })


def search_total_leyes(form, request):
    are_law = Proyecto.objects.exclude(
        titulo_de_ley__isnull=True).exclude(
        titulo_de_ley__exact='')

    obj = do_pagination(request, are_law, search=True, advanced_search=True)
    return render(request, "search_advanced/index.html", {
        "result_count": len(are_law),
        "extra_result_msg": "Total número de proyectos que han generado leyes",
        "items": obj['items'],
        "pretty_items": obj['pretty_items'],
        "first_half": obj['first_half'],
        "second_half": obj['second_half'],
        "first_page": obj['first_page'],
        "last_page": obj['last_page'],
        "current": obj['current'],
        "form": form,
        "comision": obj['comision'],
    })


def search_exonerados_dictamen(form, request):
    exonerado_de_dictamen = [i.proyecto for i in Seguimientos.objects.select_related('proyecto').filter(
        evento__icontains='exoneración de dictamen').distinct()]
    exonerado_de_dictamen = list(set(exonerado_de_dictamen))

    obj = do_pagination(request, exonerado_de_dictamen, search=True, advanced_search=True)
    return render(request, "search_advanced/index.html", {
        "result_count": len(exonerado_de_dictamen),
        "extra_result_msg": "Proyectos Exonerados de dictamen",
        "items": obj['items'],
        "pretty_items": obj['pretty_items'],
        "first_half": obj['first_half'],
        "second_half": obj['second_half'],
        "first_page": obj['first_page'],
        "last_page": obj['last_page'],
        "current": obj['current'],
        "form": form,
        "comision": obj['comision'],
    })


def search_total_aprobados(form, request):
    total_approved = [i.proyecto for i in Seguimientos.objects.select_related('proyecto').filter(
        Q(evento__icontains='promulgado') | Q(evento__icontains='publicado'))]
    total_approved = list(set(total_approved))

    obj = do_pagination(request, total_approved, search=True, advanced_search=True)
    return render(request, "search_advanced/index.html", {
        "result_count": len(total_approved),
        "extra_result_msg": "Total número de proyectos aprobados",
        "items": obj['items'],
        "pretty_items": obj['pretty_items'],
        "first_half": obj['first_half'],
        "second_half": obj['second_half'],
        "first_page": obj['first_page'],
        "last_page": obj['last_page'],
        "current": obj['current'],
        "form": form,
        "comision": obj['comision'],
    })


def search_dispensados_acuerdo_pleno(form, request):
    dispensed_by_plenary = [i.proyecto for i in Seguimientos.objects.select_related('proyecto').filter(
        evento__icontains='dispensado 2da').filter(evento__icontains='pleno')]

    obj = do_pagination(request, dispensed_by_plenary, search=True, advanced_search=True)
    return render(request, "search_advanced/index.html", {
        "result_count": len(dispensed_by_plenary),
        "extra_result_msg": "Dispensados 2da votación por acuerdo del pleno",
        "items": obj['items'],
        "pretty_items": obj['pretty_items'],
        "first_half": obj['first_half'],
        "second_half": obj['second_half'],
        "first_page": obj['first_page'],
        "last_page": obj['last_page'],
        "current": obj['current'],
        "form": form,
        "comision": obj['comision'],
    })


def search_dispensados_junta_portavoces(form, request):
    dispensed_by_spokesmen = [i.proyecto for i in Seguimientos.objects.select_related('proyecto').filter(
        evento__icontains='dispensado 2da').filter(evento__icontains='portavoces')]

    obj = do_pagination(request, dispensed_by_spokesmen, search=True, advanced_search=True)
    return render(request, "search_advanced/index.html", {
        "result_count": len(dispensed_by_spokesmen),
        "extra_result_msg": "Dispensados 2da votación por junta de portavoces",
        "items": obj['items'],
        "pretty_items": obj['pretty_items'],
        "first_half": obj['first_half'],
        "second_half": obj['second_half'],
        "first_page": obj['first_page'],
        "last_page": obj['last_page'],
        "current": obj['current'],
        "form": form,
        "comision": obj['comision'],
    })


def search_dispensados_otros(form, request):
    otros_dispensados = [i.proyecto for i in Seguimientos.objects.select_related('proyecto').filter(
        evento__icontains='dispensado 2da').exclude(
        evento__icontains='pleno').exclude(
        evento__icontains='portavoces')]

    obj = do_pagination(request, otros_dispensados, search=True, advanced_search=True)
    return render(request, "search_advanced/index.html", {
        "result_count": len(otros_dispensados),
        "extra_result_msg": "Dispensados 2da votación por otras razones",
        "items": obj['items'],
        "pretty_items": obj['pretty_items'],
        "first_half": obj['first_half'],
        "second_half": obj['second_half'],
        "first_page": obj['first_page'],
        "last_page": obj['last_page'],
        "current": obj['current'],
        "form": form,
        "comision": obj['comision'],
    })
