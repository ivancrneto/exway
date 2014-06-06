from django.conf.urls import patterns, url

urlpatterns = patterns('exway.auth.views',
    url(r'login/$', 'login', name='login'),
)
