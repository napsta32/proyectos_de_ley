from django.conf.urls import patterns, include, url
# from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', include('pdl.urls', namespace='pdl')),
    url(r'^p/', include('pdl.urls', namespace='pdl-proyecto')),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
)
