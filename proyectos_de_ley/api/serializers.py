from rest_framework import serializers

from pdl.models import Proyecto


class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = ('codigo', 'numero_proyecto', 'short_url', 'congresistas',
                  'fecha_presentacion', 'titulo', 'expediente', 'pdf_url',
                  'seguimiento_page', 'proponente', 'grupo_parlamentario',
                  'iniciativas_agrupadas', 'nombre_comision', 'titulo_de_ley',
                  'numero_de_ley')
