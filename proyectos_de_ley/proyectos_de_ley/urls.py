from django.conf.urls import patterns, include, url
from django.contrib.sitemaps.views import sitemap

from pdl.feeds import LatestEntriesFeed
from pdl.sitemaps import ProyectoSitemap
# from django.contrib import admin

sitemaps = {
    'static': ProyectoSitemap,
    }

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^', include('pdl.urls', namespace='pdl')),
    url(r'^p/', include('pdl.urls', namespace='pdl-proyecto')),
    url(r'^rss.xml$', LatestEntriesFeed(), name='pdl-rss'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    # url(r'^admin/', include(admin.site.urls)),
)

