from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from exway.core.views import PartialView, ExpensesList, ExpenseDetail

partialpatterns = patterns('',
    url(r'^expenses.html$',
        PartialView.as_view(template_name='expenses.html')),
    url(r'^reports.html$',
        PartialView.as_view(template_name='reports.html'))
)

urlpatterns = patterns('exway.core.views',
    url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),
    url(r'^api/expenses/$', ExpensesList.as_view()),
    url(r'^api/expenses/(?P<pk>[0-9]+)/$', ExpenseDetail.as_view()),
    url(r'^partials/', include(partialpatterns, namespace='partials')),
)
