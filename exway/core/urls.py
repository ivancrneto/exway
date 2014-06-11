""" Urls for core app """

from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from exway.core.views import (PartialView, ExpensesList, ExpenseDetail,
                              ExpensesAmounts, Reports)

partialpatterns = patterns(
    '',

    url(r'^expenses.html$',
        login_required(PartialView.as_view(template_name='expenses.html'))),
    url(r'^reports.html$',
        login_required(PartialView.as_view(template_name='reports.html')))
)

urlpatterns = patterns(
    'exway.core.views',

    url(r'^$', login_required(TemplateView.as_view(template_name="home.html")),
        name='home'),

    url(r'^api/expenses/$', ExpensesList.as_view(), name='expenses'),
    url(r'^api/expenses/amounts/$', ExpensesAmounts.as_view()),
    url(r'^api/expenses/(?P<pk>[0-9]+)/$', ExpenseDetail.as_view(),
        name='expense_detail'),

    url(r'^api/reports/(?P<rtype>[a-z]+)/$', Reports.as_view()),

    url(r'^partials/', include(partialpatterns, namespace='partials')),
)
