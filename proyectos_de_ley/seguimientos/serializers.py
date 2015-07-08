from rest_framework import serializers

from seguimientos.models import Iniciativas, SeguimientosJson


class IniciativasSerializer(serializers.Serializer):
    iniciativas = serializers.ListField()


class SeguimientosSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeguimientosJson
        fields = ('timeline',)

    def restore_object(self, attrs, instance=None):
        if instance:
            # Update existing instance
            instance.timeline = attrs.get('timeline', instance.timeline)
            return instance

        return SeguimientosJson(**attrs)
