from django.shortcuts import render

from pdl.models import Proyecto
from pdl.models import Seguimientos
from stats.models import ComisionCount
from stats.models import Dispensed
from stats.models import WithDictamenButNotVoted


def dame_sin_tramitar(numero_de_proyectos):
    with_seguimientos = Seguimientos.objects.values_list('proyecto_id',
                                                         flat=True).distinct().count()
    without_seguimientos = numero_de_proyectos - with_seguimientos
    percentage_without_seguimientos = round(
        (without_seguimientos * 100) / numero_de_proyectos, 1)
    return percentage_without_seguimientos, without_seguimientos


def dame_sin_dictamen(queryset, numero_de_proyectos):
    count = 0
    for i in queryset.values():
        count += i['count']
    percentage = round((count * 100) / numero_de_proyectos, 1)
    return percentage, count


def index(request):
    numero_de_proyectos = Proyecto.objects.all().count()

    with_pdf_url = Proyecto.objects.exclude(
        pdf_url__isnull=True).exclude(
        pdf_url__exact='').count()
    without_pdf_url = numero_de_proyectos - with_pdf_url
    percentage_without_pdf_url = round(
        (without_pdf_url * 100) / numero_de_proyectos, 1)

    # With dictamen sin votación
    total_dictamen_sin_votacion = WithDictamenButNotVoted.objects.count()
    percentage_dictamen_sin_votacion = round(
        (total_dictamen_sin_votacion * 100) / numero_de_proyectos, 1
    )

    # Sin Tramitar
    percentage_without_seguimientos, without_seguimientos = dame_sin_tramitar(
        numero_de_proyectos)

    # Proyectos no son ley
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

    # sin dictamen?
    percentage_total_in_commissions, total_in_commissions = dame_sin_dictamen(queryset, numero_de_proyectos)

    # Projects dispensed of 2nd round of votes
    res = Dispensed.objects.all()[0]
    dispensed_values = "[" + str(are_law) + ", " + str(res.total_approved) + ", " \
                       + str(res.total_dispensed) + ", " \
                       + str(res.dispensed_by_plenary) + ", " \
                       + str(res.dispensed_by_spokesmen) + ", " \
                       + str(res.dispensed_others) + "]"
    dispensed_categories = "['NÚMERO TOTAL DE LEYES', 'TOTAL aprobados', 'TOTAL dispensados de 2da votación', " \
                           "'Dispensados por acuerdo del pleno', " \
                           "'Dispensados por junta portavoces', " \
                           "'Otros proyectos dispensados']"

    return render(request, "stats/index.html",
                  {'percentage_without_seguimientos': percentage_without_seguimientos,
                   'percentage_total_in_commissions': percentage_total_in_commissions,
                   'total_in_commissions': total_in_commissions,

                   'total_dictamen_sin_votacion': total_dictamen_sin_votacion,
                   'percentage_dictamen_sin_votacion': percentage_dictamen_sin_votacion,

                   'numero_de_proyectos': numero_de_proyectos,
                   'without_pdf_url': without_pdf_url,
                   'percentage_without_pdf_url': percentage_without_pdf_url,
                   'without_seguimientos': without_seguimientos,
                   'are_not_law': are_not_law,
                   'percentage_are_not_law': percentage_are_not_law,
                   'comision_names': comision_names_str,
                   'comision_count': comision_count_str,
                   'dispensed_values': dispensed_values,
                   'dispensed_categories': dispensed_categories,
                   }
                  )
