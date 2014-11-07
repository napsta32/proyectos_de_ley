# -*- encoding: utf-8 -*-
from django.shortcuts import render, render_to_response
from . import forms
from pdl.models import Proyecto
from django.views.generic import CreateView


def index(request):
    if request.method == 'GET':
        form = forms.SearchAdvancedForm(request.GET)
        if form.is_valid():
            print(form)

        return render(request, 'search_advanced/index.html',
            {'form': form,})
