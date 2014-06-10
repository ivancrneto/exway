""" Urls for auth app """

from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    'exway.auth.views',

    url(r'signup/$', 'signup', name='signup'),
    url(r'login/$', 'login', name='login'),
    url(r'logout/$', 'logout', name='logout'),
    url(r'api/', include('rest_framework.urls',
                         namespace='rest_framework')),
)
