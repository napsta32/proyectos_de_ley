import json
import re
import unicodedata

from django.http import HttpResponse
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.decorators import renderer_classes
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework_csv import renderers

from pdl.models import Proyecto
from pdl.models import Seguimientos
from pdl.models import Slug
from .serializers import CongresistaSerializer
from .serializers import ExoneradoDictamenSerializer
from .serializers import Exonerados2daVotacionSerializer
from .serializers import ProyectoSerializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class CSVResponse(HttpResponse):
    """
    An HttpResponse that renders its content into CSV.
    """
    def __init__(self, data, **kwargs):
        content = CSVRenderer().render(data)
        kwargs['content_type'] = 'text/csv'
        super(CSVResponse, self).__init__(content, **kwargs)


class CSVRenderer(renderers.CSVRenderer):
    media_type = 'text/csv'
    format = 'csv'

    def render(self, data, media_type=None, renderer_context=None):
        return super(CSVRenderer, self).render(data, media_type, renderer_context)


@api_view(['GET'])
@permission_classes((AllowAny, ))
def proyecto(request, codigo):
    """
    Lista metadatos de cada proyecto de ley.
    ---
    type:
      codigo:
        required: true
        type: string

    parameters:
      - name: codigo
        description: código del proyecto de ley incluyendo legislatura, por ejemplo 00002-2011
        type: string
        paramType: path
        required: true
    """
    # TODO: hay que agregar un campo a la tabla especificando si es legislatura 2011 o cual.
    # luego corregir aquí el API
    codigo = re.sub('-[0-9]+', '', codigo)
    try:
        proy = Proyecto.objects.get(numero_proyecto__startswith=codigo)
    except Proyecto.DoesNotExist:
        msg = {'error': 'proyecto no existe'}
        return HttpResponse(json.dumps(msg), content_type='application/json')

    if request.method == 'GET':
        serializer = ProyectoSerializer(proy)
        return JSONResponse(serializer.data)


@api_view(['GET'])
@permission_classes((AllowAny, ))
def congresista(request, nombre_corto):
    """
    Lista proyectos de ley de cada congresista.

    # Por ejemplo:

    * <http://proyectosdeley.pe/api/congresista.json/Manuel+Zerillo/>

    # Puedes obtener los resultados en archivo CSV (fácil de importar a MS Excel)

    Solo es necesario usar la dirección `congresista.csv`:

    * <http://proyectosdeley.pe/api/congresista.csv/Manuel+Zerillo/>
    ---
    type:
      nombre_corto:
        required: true
        type: string

    parameters:
      - name: nombre_corto
        description: Nombre y apellido del congresista, por ejemplo<br /> Manuel+Zerillo
        type: string
        paramType: path
        required: true
    """
    nombre_corto = nombre_corto.replace('+', ' ')
    names = find_name_from_short_name(nombre_corto)

    if '---error---' in names:
        msg = {'error': names[1]}
        return HttpResponse(json.dumps(msg), content_type='application/json')

    projects_and_person = get_projects_for_person(names)
    data = {
        'resultado': projects_and_person,
        'numero_de_congresistas': len(projects_and_person),
    }
    if request.method == 'GET':
        serializer = CongresistaSerializer(data)
        return JSONResponse(serializer.data)


@permission_classes((AllowAny,))
@renderer_classes((CSVRenderer,))
def congresista_csv(request, nombre_corto):
    """
    Lista proyectos de ley de cada congresista.

    # Por ejemplo:

    * <http://proyectosdeley.pe/api/congresista.csv/Manuel+Zerillo/>
    ---
    type:
      nombre_corto:
        required: true
        type: string
        omit_serializer: true

    parameters:
      - name: nombre_corto
        description: Nombre y apellido del congresista, por ejemplo<br /> Manuel+Zerillo
        type: string
        paramType: path
        required: true
    """
    nombre_corto = nombre_corto.replace('+', ' ')
    names = find_name_from_short_name(nombre_corto)

    if '---error---' in names:
        msg = 'error,{}'.format(names[1])
        return HttpResponse(msg, content_type='text/csv')

    projects_and_person = get_projects_for_person(names)
    data = []
    for i in projects_and_person:
        for p in i['proyectos']:
            data.append({'proyecto': p, 'nombre': i['nombre']})
    if request.method == 'GET':
        return CSVResponse(data)


def get_projects_for_person(names):
    projects_and_person = []
    for name in names:
        queryset = Proyecto.objects.filter(
            congresistas__icontains=name).order_by('-codigo')
        projects_list = [str(i.codigo) + '-2011' for i in queryset]
        obj = {'nombre': name, 'proyectos': projects_list}
        projects_and_person.append(obj)
    return projects_and_person


@api_view(['GET'])
@permission_classes((AllowAny, ))
def congresista_y_comision(request, nombre_corto, comision):
    """
    Lista proyectos de ley de cada congresista.

    # Por ejemplo:

    * <http://proyectosdeley.pe/api/congresista.json/Manuel+Zerillo/>
    * <http://proyectosdeley.pe/api/congresista.json/Manuel+Zerillo/Economía/>
    ---
    type:
      nombre_corto:
        required: true
        type: string
      comision:
        required: true
        type: string

    parameters:
      - name: nombre_corto
        description: Nombre y apellido del congresista, por ejemplo<br /> Manuel+Zerillo
        type: string
        paramType: path
        required: true
      - name: comision
        description: Comisión congresal, por ejemplo<br /> Economía
        type: string
        paramType: path
        required: true
    """
    nombre_corto = nombre_corto.replace('+', ' ')
    names = find_name_from_short_name(nombre_corto)

    if '---error---' in names:
        msg = {'error': names[1]}
        return HttpResponse(json.dumps(msg), content_type='application/json')

    comision = comision.strip()
    projects_and_person = get_projects_by_comission_for_person(comision, names)
    data = {
        'resultado': projects_and_person,
        'numero_de_congresistas': len(projects_and_person),
    }
    if request.method == 'GET':
        serializer = CongresistaSerializer(data)
        return JSONResponse(serializer.data)


@permission_classes((AllowAny, ))
@renderer_classes((CSVRenderer,))
def congresista_y_comision_csv(request, nombre_corto, comision):
    """
    Lista proyectos de ley de cada congresista.

    # Por ejemplo:

    * <http://proyectosdeley.pe/api/congresista.csv/Manuel+Zerillo/>
    * <http://proyectosdeley.pe/api/congresista.csv/Manuel+Zerillo/Economía/>
    ---
    type:
      nombre_corto:
        required: true
        type: string
      comision:
        required: true
        type: string

    parameters:
      - name: nombre_corto
        description: Nombre y apellido del congresista, por ejemplo<br /> Manuel+Zerillo
        type: string
        paramType: path
        required: true
      - name: comision
        description: Comisión congresal, por ejemplo<br /> Economía
        type: string
        paramType: path
        required: true
    """
    nombre_corto = nombre_corto.replace('+', ' ')
    names = find_name_from_short_name(nombre_corto)

    if '---error---' in names:
        msg = {'error': names[1]}
        return HttpResponse(json.dumps(msg), content_type='application/json')

    comision = comision.strip()
    projects_and_person = get_projects_by_comission_for_person(comision, names)
    data = []
    for i in projects_and_person:
        for p in i['proyectos']:
            data.append({'proyecto': p, 'nombre': i['nombre']})
    if request.method == 'GET':
        return CSVResponse(data)


def get_projects_by_comission_for_person(comision, names):
    projects_and_person = []
    for name in names:
        queryset = Proyecto.objects.filter(
            congresistas__icontains=name).order_by('-codigo')
        if comision != '':
            queryset = queryset.filter(nombre_comision__icontains=comision)
        projects_list = [str(i.codigo) + '-2011' for i in queryset]
        obj = {'nombre': name, 'proyectos': projects_list}
        projects_and_person.append(obj)
    return projects_and_person


@api_view(['GET'])
@permission_classes((AllowAny, ))
def exonerados_dictamen(request):
    """
    Lista proyectos que han sido aprobados y exonerados de dictamen.
    """
    exonerado_de_dictamen = ['{}-2011'.format(i.proyecto.codigo)
                             for i in Seguimientos.objects.select_related('proyecto').filter(
                             evento__icontains='exoneración de dictamen').distinct()]
    exonerado_de_dictamen = list(set(exonerado_de_dictamen))

    if len(exonerado_de_dictamen) > 0:
        data = {'resultado': exonerado_de_dictamen}
        if request.method == 'GET':
            serializer = ExoneradoDictamenSerializer(data)
            return JSONResponse(serializer.data)
    else:
        msg = {'error': 'no se encontraron resultados'}
        return HttpResponse(json.dumps(msg), content_type='application/json')


@api_view(['GET'])
@permission_classes((AllowAny, ))
def exonerados_2da_votacion(request):
    """
    Lista proyectos que han sido exonerados de 2da votación en el pleno.
    ---
    """
    total_dispensed = ["{}-2011".format(i.proyecto.codigo)
                       for i in Seguimientos.objects.select_related('proyecto').filter(
                       evento__icontains='dispensado 2da')]

    if len(total_dispensed) > 0:
        data = {'resultado': total_dispensed}
        if request.method == 'GET':
            serializer = Exonerados2daVotacionSerializer(data)
            return JSONResponse(serializer.data)
    else:
        msg = {'error': 'no se encontraron resultados'}
        return HttpResponse(json.dumps(msg), content_type='application/json')


def find_name_from_short_name(nombre_corto):
    nombre_corto = unicodedata.normalize('NFKD', nombre_corto).encode('ascii', 'ignore')
    nombre_corto = re.sub('\s+', ' ', nombre_corto.decode('utf-8'))
    nombre_corto = nombre_corto.split(' ')
    if len(nombre_corto) < 2:
        return ['---error---', 'ingrese un nombre y un apellido']

    nombre_corto = nombre_corto[:2]
    res = Slug.objects.filter(Q(ascii__icontains=nombre_corto[0]) & Q(ascii__icontains=nombre_corto[1]))

    if len(res) > 0:
        return [i.nombre for i in res]
    else:
        return ['---error---', 'no se pudo encontrar congresista']
