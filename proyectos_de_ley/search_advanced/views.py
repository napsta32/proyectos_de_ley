# -*- encoding: utf-8 -*-
from django.shortcuts import render

from . import forms
from pdl.models import Proyecto
from pdl.models import Seguimientos
from pdl.utils import do_pagination
from pdl.utils import convert_date_to_string


def index(request):
    if request.method == 'GET':
        form = forms.SearchAdvancedForm(request.GET)
        if form.is_valid():
            if form.cleaned_data['date_from'] is not None:
                date_from = form.cleaned_data['date_from']
                date_to = form.cleaned_data['date_to']
                queryset = Proyecto.objects.filter(fecha_presentacion__range=[date_from, date_to]).order_by('-codigo')

                obj = do_pagination(request, queryset, search=True, advanced_search=True)
                return render(request, "search_advanced/index.html", {
                    "items": obj['items'],
                    "pretty_items": obj['pretty_items'],
                    "first_half": obj['first_half'],
                    "second_half": obj['second_half'],
                    "first_page": obj['first_page'],
                    "last_page": obj['last_page'],
                    "current": obj['current'],
                    "form": form,
                    "date_from": convert_date_to_string(date_from),
                    "date_to": convert_date_to_string(date_to),
                }
                )
            if form.cleaned_data['comision'].strip() != '':
                comision = form.cleaned_data['comision']
                if comision.lower() == 'ciencia':
                    comision = 'Ciencia'
                queryset = Seguimientos.objects.order_by('-proyecto_id')
                proyectos = Proyecto.objects.order_by('-codigo')

                proyects_found = []

                this_proyecto_id = ''
                for i in queryset:
                    if i.proyecto_id != this_proyecto_id:
                        if comision in i.evento:
                            for proyecto in proyectos:
                                if i.proyecto_id == proyecto.id:
                                    proyects_found.append(proyecto)
                                    continue
                    this_proyecto_id = i.proyecto_id

                obj = do_pagination(request, proyects_found, search=True, advanced_search=True)
                return render(request, "search_advanced/index.html", {
                    "items": obj['items'],
                    "pretty_items": obj['pretty_items'],
                    "first_half": obj['first_half'],
                    "second_half": obj['second_half'],
                    "first_page": obj['first_page'],
                    "last_page": obj['last_page'],
                    "current": obj['current'],
                    "form": form,
                })

            return render(request, "search_advanced/index.html", {
                "form": form,
            })

        else:
            return render(request, "search_advanced/index.html", {
                "form": form,
            })
