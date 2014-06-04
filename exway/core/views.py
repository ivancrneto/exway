from django.views.generic import TemplateView
from .models import Expense
from .serializers import ExpenseSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class PartialView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(PartialView, self).get_context_data(**kwargs)
        return context


class ExpensesList(APIView):
    """ Class responsible for listing all expenses or create a new one """
    def get(self, request, format=None):
        expenses = Expense.objects.order_by('created_on')
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)
