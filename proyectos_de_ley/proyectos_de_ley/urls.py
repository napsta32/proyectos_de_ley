from django.conf.urls import patterns, include, url
from django.contrib.sitemaps.views import sitemap

from pdl.feeds import LatestEntriesFeed
from pdl.sitemaps import ProyectoSitemap, CongresistaSitemap
from seguimientos import views as seg_views
# from django.contrib import admin
from rest_framework import routers

sitemaps = {
    'static': ProyectoSitemap,
    'congresista': CongresistaSitemap,
    }

urlpatterns = patterns(
    '',
    # api for AJAX get request
    url(r'^', include('pdl.urls', namespace='pdl')),
    url(r'^stats', include('stats.urls', namespace='stats')),
    url(r'^p/', include('pdl.urls', namespace='pdl-proyecto')),
    url(r'^p/(?P<short_url>[0-9a-z]+/seguimiento/)', seg_views.index),
    url(r'^rss.xml$', LatestEntriesFeed(), name='pdl-rss'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),

    url(r'^api/iniciativas/', include('seguimientos.urls')),
    # url(r'^admin/', include(admin.site.urls)),
)
