from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^(?P<short_url>[0-9a-z]+)/seguimiento/$', views.index, name='index'),

    url(r'^iniciativas/(?P<short_url>[0-9a-z]+)/$', views.iniciativa_list),
    url(r'^seguimientos/(?P<short_url>[0-9a-z]+)/$', views.seguimientos_list),
)
