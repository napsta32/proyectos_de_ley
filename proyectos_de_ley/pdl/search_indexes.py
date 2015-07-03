import re
import unicodedata

from haystack import indexes

from .models import Proyecto


class ProyectoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    codigo = indexes.CharField(model_attr='codigo', null=True)
    numero_proyecto = indexes.CharField(model_attr='numero_proyecto', null=True)
    short_url = indexes.CharField(model_attr='short_url', null=True)
    congresistas = indexes.EdgeNgramField(model_attr='congresistas', null=True)
    titulo = indexes.EdgeNgramField(model_attr='titulo', null=True)
    titulo_de_ley = indexes.EdgeNgramField(model_attr='titulo_de_ley', null=True)
    numero_de_ley = indexes.CharField(model_attr='titulo_de_ley', null=True)

    def prepare_codigo(self, obj):
        codigo = obj.codigo
        codigo_truncado = re.sub('^0+', '', codigo)
        return codigo_truncado

    def prepare_congresistas(self, obj):
        result = self.normalize_field(obj.congresistas)
        return result

    def prepare_titulo(self, obj):
        result = self.normalize_field(obj.titulo)
        return result

    def prepare_titulo_de_ley(self, obj):
        try:
            result = self.normalize_field(obj.titulo_de_ley)
        except TypeError:
            return ''
        return result

    def normalize_field(self, value):
        original = value
        modified = unicodedata.normalize('NFKD', original).encode('ascii', 'ignore')
        result = ' '.join([original, modified.decode(encoding='utf-8')])
        return result

    def get_model(self):
        return Proyecto
