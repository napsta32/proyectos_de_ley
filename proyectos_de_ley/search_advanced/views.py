# -*- encoding: utf-8 -*-
import datetime

from django.shortcuts import render, render_to_response
from . import forms
from pdl.models import Proyecto
from pdl.views import do_pagination
from django.views.generic import CreateView


def index(request):
    if request.method == 'GET':
        form = forms.SearchAdvancedForm(request.GET)
        if form.is_valid():
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            queryset = Proyecto.objects.filter(fecha_presentacion__range=[date_from, date_to])

            obj = do_pagination(request, queryset, search=True)
            print(obj)
            return render(request, "search_advanced/index.html", {
                "items": obj['items'],
                "pretty_items": obj['pretty_items'],
                "first_half": obj['first_half'],
                "second_half": obj['second_half'],
                "first_page": obj['first_page'],
                "last_page": obj['last_page'],
                "current": obj['current'],
                "form": form,
                "date_from": convert_date(date_from),
                "date_to": convert_date(date_to),
                }
            )

def convert_date(fecha):
    return datetime.date.strftime(fecha, '%m/%d/%Y')

