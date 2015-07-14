from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^proyecto/(?P<codigo>[0-9]+\-[0-9]+)/$', views.proyecto),
    url(r'^congresista.json/(?P<nombre_corto>.+)/$', views.congresista),
    url(r'^congresista.tsv/(?P<nombre_corto>.+)/$', views.congresista_tsv),
    url(r'^congresista_y_comision/(?P<nombre_corto>.+)/(?P<comision>.+)/$', views.congresista_y_comision),
    url(r'^exonerados_dictamen/$', views.exonerados_dictamen),
    url(r'^exonerados_2da_votacion/$', views.exonerados_2da_votacion),
)
