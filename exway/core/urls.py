from django.conf.urls import patterns, include, url
from exway.core.views import PartialView

partialpatterns = patterns('',
    url(r'^expenses.html$',
        PartialView.as_view(template_name='expenses.html')),
    url(r'^reports.html$',
        PartialView.as_view(template_name='reports.html'))
)

urlpatterns = patterns('exway.core.views',
    url(r'^$', 'home', name='home'),
    url(r'^partials/', include(partialpatterns, namespace='partials')),
)
