# -*- encoding: utf-8 -*-
import datetime

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed

from pdl.models import Proyecto


class CorrectMimeTypeFeed(Rss201rev2Feed):
    mime_type = 'application/xml'


class LatestEntriesFeed(Feed):
    title = 'Proyectos de ley emitidos por el Congreso de la República del' \
            ' Perú'
    link = 'http://www.proyectosdeley.pe/rss.xml'
    description = 'proyectosdeley.pe es un intento de transparentar el Cong' \
                  'reso y poner al alcance de la mayor cantidad de personas' \
                  'los proyectos de ley presentados y discutidos en el parl' \
                  'amento. La información mostrada es tomada directamente d' \
                  'e la página web del Congreso.'
    feed_type = CorrectMimeTypeFeed

    def items(self):
        return Proyecto.objects.order_by('-codigo')

    def item_title(self, item):
        return item.titulo[:140] + "..."

    def item_description(self, item):
        out = item.titulo + '<br /><br />Autores: '
        out += item.congresistas + '<br /><br />'
        out += '<a href="' + item.pdf_url + '">PDF</a> '
        out += '<a href="' + item.expediente + '">Expediente</a>'
        return out

    def item_link(self, item):
        return 'http://www.proyectosdeley.pe/p/' + item.short_url

    def item_pubdate(self, item):
        # TODO make sure scrapy saves a datetime object into our database
        # so we can avoid this exception catching
        try:
            time_object = datetime.datetime.strptime(item.time_created, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            time_object = datetime.datetime.strptime(item.time_created, "%Y-%m-%d %H:%M:%S")

        return time_object
