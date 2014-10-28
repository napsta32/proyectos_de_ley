from django.forms import widgets
from rest_framework import serializers

from seguimientos.models import Iniciativas, SeguimientosJson


class IniciativasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Iniciativas
        fields = ('nodes',)

    def restore_object(self, attrs, instance=None):
        if instance:
            # Update existing instance
            instance.nodes = attrs.get('nodes', instance.nodes)
            return instance

        return Iniciativas(**attrs)


class SeguimientosSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeguimientosJson
        fields = ('headline', 'date', 'type', 'text',)

    def restore_object(self, attrs, instance=None):
        if instance:
            # Update existing instance
            instance.headline = attrs.get('headline', instance.headline)
            return instance

        return SeguimientosJson(**attrs)
