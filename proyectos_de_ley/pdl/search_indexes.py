import re
import unicodedata

from haystack import indexes

from .models import Proyecto


class ProyectoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    codigo = indexes.CharField(model_attr='codigo')
    titulo = indexes.EdgeNgramField(model_attr='titulo', null=True)

    """
    def prepare_text(self, obj):
        codigo = obj.codigo
        codigo_truncado = re.sub('^0+', '', codigo)
        fields = [codigo, codigo_truncado, obj.numero_proyecto, obj.short_url,
                  obj.congresistas, obj.titulo, obj.titulo_de_ley, obj.numero_de_ley]
        data = []
        for i in fields:
            if i is not None:
                data.append(i)

        original = ' '.join(data)
        modified = unicodedata.normalize('NFD', original).encode('ascii', 'ignore')
        result = ' '.join([original, modified.decode(encoding='utf-8')])
        return result
    """
    def prepare_titulo(self, obj):
        original = obj.titulo
        modified = unicodedata.normalize('NFKD', original).encode('ascii', 'ignore')
        result = ' '.join([original, modified.decode(encoding='utf-8')])
        return result

    def get_model(self):
        return Proyecto
