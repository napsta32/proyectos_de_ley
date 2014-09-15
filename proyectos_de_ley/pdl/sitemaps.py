from django.contrib.sitemaps import Sitemap

from pdl.models import Proyecto


class ProyectoSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return Proyecto.objects.order_by('-codigo')

    def lastmod(self, item):
        return item.time_created

    def location(self, item):
        loc = '/p/' + item.short_url + '/'
        return loc