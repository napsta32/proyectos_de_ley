from django.shortcuts import render

from pdl.models import Proyecto


def index(request):
    numero_de_proyectos = Proyecto.objects.all().count()

    without_pdf_url = Proyecto.objects.filter(pdf_url='').count()
    percentage_withouth_pdf_url = round(without_pdf_url/numero_de_proyectos, 2)

    return render(request, "stats/index.html",
                  {'numero_de_proyectos': numero_de_proyectos,
                   'without_pdf_url': without_pdf_url,
                   'percentage_without_pdf_url': percentage_withouth_pdf_url})
