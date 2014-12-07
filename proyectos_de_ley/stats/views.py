from django.shortcuts import render

from pdl.models import Proyecto
from pdl.models import Seguimientos
from stats.models import ComisionCount
from stats.models import Dispensed


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

    # Projects by comision count
    queryset = ComisionCount.objects.all().order_by('-count')
    comision_names_str = "['"
    comision_count_str = "["
    for i in queryset:
        comision_names_str += str(i.comision) + "', '"
        comision_count_str += str(i.count) + ", "

    comision_names_str += "']"
    comision_count_str += "]"

    # Projects dispensed of 2nd round of votes
    res = Dispensed.objects.all()[0]
    dispensed_values = "[" + str(res.total_approved) + ", " \
                       + str(res.total_dispensed) + ", " \
                       + str(res.dispensed_by_plenary) + ", " \
                       + str(res.dispensed_by_spokesmen) + ", " \
                       + str(res.dispensed_others) + "]"
    dispensed_categories = "['TOTAL aprobados', 'TOTAL dispensados de 2da votación', " \
                           "'Dispensados por acuerdo del pleno', " \
                           "'Dispensados por junta portavoces', " \
                           "'Otros proyectos dispensados']"
    print(dispensed_categories)

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
                   'comision_names': comision_names_str,
                   'comision_count': comision_count_str,
                   'dispensed_values': dispensed_values,
                   'dispensed_categories': dispensed_categories,
                   }
                  )
