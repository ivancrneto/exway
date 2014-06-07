from django.views.generic import TemplateView
from django.http import Http404
from .models import Expense
from .serializers import ExpenseSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from exway.core.permissions import IsOwner


class PartialView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(PartialView, self).get_context_data(**kwargs)
        return context


class ExpensesList(APIView):
    """ Class responsible for listing all expenses or create a new one """

    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get(self, request, format=None):
        """ method for retrieving expenses """
        expenses = Expense.objects.filter(user=
                                          request.user).order_by('created_on')
        serializer = ExpenseSerializer(expenses, request=request, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """ method for creating new expenses """
        serializer = ExpenseSerializer(data=request.DATA, request=request)
        self.check_object_permissions(request, serializer.object)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseDetail(APIView):
    """ Class responsible for updating or deleting an expense """

    permission_classes = (permissions.IsAuthenticated, IsOwner,)

    def get_object(self, pk):
        try:
            return Expense.objects.get(pk=pk)
        except Expense.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """ method for retrieving one expense """
        expense = self.get_object(pk)
        serializer = ExpenseSerializer(expense, request=request)
        self.check_object_permissions(request, serializer.object)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """ method for updating one expense """
        expense = self.get_object(pk)
        serializer = ExpenseSerializer(expense, data=request.DATA,
                                       request=request)
        self.check_object_permissions(request, serializer.object)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """ mathod for deleting one expense """
        expense = self.get_object(pk)
        self.check_object_permissions(request, expense)
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
