from django.shortcuts import render

from pdl.models import Proyecto
from pdl.models import Seguimientos


def index(request):
    numero_de_proyectos = Proyecto.objects.all().count()

    with_pdf_url = Proyecto.objects.exclude(
        pdf_url__isnull=True).exclude(
        pdf_url__exact='').count()
    without_pdf_url = numero_de_proyectos - with_pdf_url
    percentage_without_pdf_url = round(
        (without_pdf_url * 100) / numero_de_proyectos, 1)

    with_iniciativas = Proyecto.objects.exclude(
        iniciativas_agrupadas__isnull=True).exclude(
        iniciativas_agrupadas__exact='').count()
    without_iniciativas = numero_de_proyectos - with_iniciativas
    percentage_without_iniciativas = round(
        (without_iniciativas * 100) / numero_de_proyectos, 1)

    with_seguimientos = Seguimientos.objects.values_list('proyecto_id', flat=True).distinct().count()
    without_seguimientos = numero_de_proyectos - with_seguimientos
    percentage_without_seguimientos = round(
        (without_seguimientos * 100) / numero_de_proyectos, 1)

    are_law = Proyecto.objects.exclude(
        titulo_de_ley__isnull=True).exclude(
        titulo_de_ley__exact='').count()
    are_not_law = numero_de_proyectos - are_law
    percentage_are_not_law = round(
        (are_not_law * 100) / numero_de_proyectos, 1)

    return render(request, "stats/index.html",
                  {'numero_de_proyectos': numero_de_proyectos,
                   'without_pdf_url': without_pdf_url,
                   'percentage_without_pdf_url': percentage_without_pdf_url,
                   'without_iniciativas': without_iniciativas,
                   'percentage_without_iniciativas': percentage_without_iniciativas,
                   'without_seguimientos': without_seguimientos,
                   'percentage_without_seguimientos': percentage_without_seguimientos,
                   'are_not_law': are_not_law,
                   'percentage_are_not_law': percentage_are_not_law,
                   }
                  )
