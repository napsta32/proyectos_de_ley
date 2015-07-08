from rest_framework import serializers

from pdl.models import Proyecto


class ProyectoSerializer(serializers.ModelSerializer):
    fecha_presentacion = serializers.DateTimeField(format=None)

    class Meta:
        model = Proyecto
        fields = ('codigo', 'numero_proyecto', 'short_url', 'congresistas',
                  'fecha_presentacion', 'titulo', 'expediente', 'pdf_url',
                  'seguimiento_page', 'proponente', 'grupo_parlamentario',
                  'iniciativas_agrupadas', 'nombre_comision', 'titulo_de_ley',
                  'numero_de_ley')


class CongresistaSerializer(serializers.Serializer):
    congresista = serializers.CharField(max_length=250)
    proyectos = serializers.ListField()
