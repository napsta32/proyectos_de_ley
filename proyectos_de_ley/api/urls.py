from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^proyecto/(?P<codigo>[0-9]+\-[0-9]+)/$', views.proyecto),
    url(r'^congresista/', views.congresista),
    url(r'^exonerados_dictamen/$', views.exonerados_dictamen),
    url(r'^exonerados_2da_votacion/$', views.exonerados_2da_votacion),
)
