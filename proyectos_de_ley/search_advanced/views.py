# -*- encoding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.contrib.formtools.wizard.views import WizardView


class SearchWizard(WizardView):
    def done(self, form_list, **kwargs):
        return render_to_response('done.html', {
            'form_data': [form.cleaned_data for form in form_list]
        })


def index(request):
    return render(request, "search_advanced/index.html")
