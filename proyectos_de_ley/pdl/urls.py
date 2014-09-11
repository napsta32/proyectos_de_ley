from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^search/$', views.search, name='search'),
    url(r'^(?P<short_url>[0-9a-z]+)/$', views.proyecto),
    # url(r'^search/$', views.search, name='search'),
    # url(r'^search?q=(?P<query>.+)$', views.search, name='search'),
)
