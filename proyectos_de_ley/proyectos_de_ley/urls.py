from django.conf.urls import patterns, include, url
from pdl.feeds import LatestEntriesFeed
# from django.contrib import admin

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^', include('pdl.urls', namespace='pdl')),
    url(r'^p/', include('pdl.urls', namespace='pdl-proyecto')),
    url(r'^rss.xml$', LatestEntriesFeed(), name='pdl-rss'),
    # url(r'^admin/', include(admin.site.urls)),
)
