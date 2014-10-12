from django.forms import widgets
from rest_framework import serializers

from pdl.models import Proyecto


class IniciativasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = ('short_url', 'iniciativas_agrupadas')

    def restore_object(self, attrs, instance=None):
        if instance:
            # Update existing instance
            instance.short_url = attrs.get('short_url', instance.short_url)
            instance.iniciativas_agrupadas = attrs.get('iniciativas_agrupadas',
                                                      instance.iniciativas_agrupadas)
            return instance

        return Proyecto(**attrs)
