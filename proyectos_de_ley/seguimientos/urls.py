from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^(?P<short_url>[0-9a-z]+)/seguimiento/$', views.index, name='index'),
)
