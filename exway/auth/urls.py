from django.conf.urls import patterns, url

urlpatterns = patterns('exway.auth.views',
    # url(r'signup/$', 'signup', name='signup'),
    url(r'login/$', 'login', name='login'),
    # url(r'logout/$', 'logout', name='logout'),
)
