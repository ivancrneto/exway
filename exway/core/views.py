""" Views for core app """

from datetime import datetime
from isoweek import Week
from decimal import Decimal
from django.views.generic import TemplateView
from django.db.models import Q, Avg, Sum, Count, Max, Min
from django.http import Http404
from .models import Expense
from .serializers import ExpenseSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from exway.core.permissions import IsOwner


class PartialView(TemplateView):
    """ Class for processing requests for templates from the client """

    def get_context_data(self, **kwargs):
        """ Method for updating template context data and do some verifications
        """
        if not self.request.is_ajax():
            raise Http404

        context = super(PartialView, self).get_context_data(**kwargs)
        return context


class ExpensesList(APIView):
    """ Class responsible for listing all expenses or create a new one """

    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def apply_filter(self, request):
        """ Applies the filters when expenses filters are used """
        description = request.GET.get('description')
        comment = request.GET.get('comment')
        amount_min = request.GET.get('amountMin')
        amount_max = request.GET.get('amountMax')
        date_from = request.GET.get('dateFrom')
        date_to = request.GET.get('dateTo')

        query = Q()
        if description:
            query &= Q(description__contains=description)
        if comment:
            query &= Q(comment__contains=comment)
        if amount_min:
            query &= Q(amount__gte=Decimal(amount_min))
        if amount_max:
            query &= Q(amount__lte=Decimal(amount_max))
        if date_from:
            date_from = datetime.strptime(date_from, '%Y-%m-%d')
            query &= Q(datetime__gte=date_from)
        if date_to:
            date_to = datetime.strptime(date_to, '%Y-%m-%d')
            date_to = date_to.replace(hour=23, minute=59, second=59)
            query &= Q(datetime__lte=date_to)

        return query

    def get(self, request, format=None):
        """ Method for retrieving expenses """
        expenses = Expense.objects.filter(Q(user=request.user) &
                                          self.apply_filter(request))
        expenses = expenses.order_by('datetime')
        serializer = ExpenseSerializer(expenses, request=request, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """ Method for creating new expenses """
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
        """ Gets a single expense object """
        try:
            return Expense.objects.get(pk=pk)
        except Expense.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """ Method for retrieving one expense """
        expense = self.get_object(pk)
        serializer = ExpenseSerializer(expense, request=request)
        self.check_object_permissions(request, serializer.object)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """ Method for updating one expense """
        expense = self.get_object(pk)
        serializer = ExpenseSerializer(expense, data=request.DATA,
                                       request=request)
        self.check_object_permissions(request, serializer.object)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """ Method for deleting one expense """
        expense = self.get_object(pk)
        self.check_object_permissions(request, expense)
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExpensesAmounts(APIView):
    """ Class for getting maximum and minimum expenses amounts """

    permission_classes = (permissions.IsAuthenticated, IsOwner,)

    def get(self, request, format=None):
        """ Gets the minimum and max expense amounts for the user """
        amounts = Expense.objects.filter(user=request.user).aggregate(
            max=Max('amount'), min=Min('amount'))
        return Response(amounts)


class Reports(APIView):
    """ Class responsible for generating expenses reports """

    permission_classes = (permissions.IsAuthenticated, IsOwner,)

    def get(self, request, rtype, format=None):
        """ Handles the GET call from the API """
        if rtype == 'weekly':
            return self.weekly_report(request)

        raise Http404

    def weekly_report(self, request):
        """ Gets data from database and formats weekly report """
        # weeks sum and average aggregation
        # NOTE: only works with sqlite
        weeks = Expense.objects.filter(user=request.user).extra({
            "week": "strftime('%Y%W', datetime)"}).values('week').\
            order_by('week').annotate(total=Sum('amount'),
                                      average=Avg('amount'),
                                      count=Count('amount'))
        weeks = {w['week']: w for w in weeks}

        # expenses per week
        # NOTE: only works with sqlite
        weeks_expenses = Expense.objects.filter(user=request.user).extra(
            {"week": "strftime('%Y%W', datetime)"}).order_by('datetime')

        # adjusting data
        for expense in weeks_expenses:
            week = weeks[expense.week]
            if 'expenses' not in week:
                week['expenses'] = []
            week['expenses'].append(ExpenseSerializer(expense).data)

            week['initialDate'] = Week(int(week['week'][:4]),
                                       int(week['week'][4:]) + 1).monday()
            week['finalDate'] = Week(int(week['week'][:4]),
                                     int(week['week'][4:]) + 1).sunday()

        return Response(sorted(weeks.values(), key=lambda x: x['week']))
