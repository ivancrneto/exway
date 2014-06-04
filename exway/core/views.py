from django.views.generic import TemplateView
from .models import Expense
from .serializers import ExpenseSerializer


class PartialView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(PartialView, self).get_context_data(**kwargs)
        return context
