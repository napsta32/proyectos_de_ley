from django.forms import widgets
from rest_framework import serializers

from pdl.models import Proyecto


class IniciativasSerializer(serializers.Serializer):
    pk = serializers.Field()
    codigo = serializers.CharField(required=True, max_length=100)
    iniciativas_agrupadas = serializers.CharField(widget=widgets.Textarea,
                                                  max_length=1000000)

    def restore_object(self, attrs, instance=None):
        if instance:
            # Update existing instance
            instance.codigo = attrs.get('codigo', instance.codigo)
            instance.iniciativas_agrupadas = attrs.get('codigo',
                                                      instance.iniciativas_agrupadas)
            return instance

        return Proyecto(**attrs)
