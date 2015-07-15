from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^proyecto.json/(?P<codigo>[0-9]+\-[0-9]+)/$', views.proyecto),

    url(r'^congresista.json/(?P<nombre_corto>.+)/$', views.congresista),
    url(r'^congresista.csv/(?P<nombre_corto>.+)/$', views.congresista_csv),

    url(r'^congresista_y_comision.json/(?P<nombre_corto>.+)/(?P<comision>.+)/$', views.congresista_y_comision),
    url(r'^congresista_y_comision.csv/(?P<nombre_corto>.+)/(?P<comision>.+)/$', views.congresista_y_comision_csv),

    url(r'^exonerados_dictamen.json/$', views.exonerados_dictamen),
    url(r'^exonerados_2da_votacion.json/$', views.exonerados_2da_votacion),
)
