""" Project urls """

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'', include('exway.core.urls', namespace='core')),
    url(r'^auth/', include('exway.auth.urls', namespace='auth')),
    url(r'^admin/', include(admin.site.urls)),
)
