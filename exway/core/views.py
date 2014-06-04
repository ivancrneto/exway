from django.views.generic import TemplateView
from .models import Expense
from .serializers import ExpenseSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class PartialView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(PartialView, self).get_context_data(**kwargs)
        return context


class ExpensesList(APIView):
    """ Class responsible for listing all expenses or create a new one """
    def get(self, request, format=None):
        """ method for retrieving expenses """
        expenses = Expense.objects.order_by('created_on')
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """ method for creating new expenses """
        serializer = ExpenseSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
