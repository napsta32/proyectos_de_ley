import unicodedata

from haystack import indexes

from .models import Proyecto


class ProyectoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    date = indexes.DateField(model_attr='fecha_presentacion', null=True)

    def prepare_text(self, obj):
        data = [obj.codigo, obj.titulo]
        original = ' '.join(data)
        modified = unicodedata.normalize('NFD', original).encode('ascii', 'ignore')
        result = ' '.join([original, modified.decode(encoding='utf-8')])
        return result

    def get_model(self):
        return Proyecto
