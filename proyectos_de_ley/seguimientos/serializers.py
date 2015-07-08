from rest_framework import serializers


class IniciativasSerializer(serializers.Serializer):
    iniciativas = serializers.ListField()


class SeguimientosSerializer(serializers.Serializer):
    timeline = serializers.DictField()
