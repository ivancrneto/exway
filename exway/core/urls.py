from django.conf.urls import patterns, include, url

urlpatterns = patterns('exway.core.views',
    url(r'^$', 'home', name='home'),
)
