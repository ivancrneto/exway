from django.shortcuts import render
from django.views.generic import TemplateView


class PartialView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(PartialView, self).get_context_data(**kwargs)
        return context


def home(request):
    """ This view just returns the html for the draw page """
    return render(request, 'home.html', {})
