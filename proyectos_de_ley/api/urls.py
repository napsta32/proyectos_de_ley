from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^proyecto/(?P<codigo>[0-9]+\-[0-9]+)/$', views.proyecto),
)
