from django.conf.urls import url

from search_advanced.views import index


urlpatterns = [
    url(r'^$', index),
]
