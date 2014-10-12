from django.forms import widgets
from rest_framework import serializers

from seguimientos.models import Iniciativas


class IniciativasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Iniciativas
        fields = ('nodes', 'links')

    def restore_object(self, attrs, instance=None):
        if instance:
            # Update existing instance
            instance.nodes = attrs.get('nodes', instance.nodes)
            instance.links = attrs.get('links', instance.links)
            return instance

        return Iniciativas(**attrs)
