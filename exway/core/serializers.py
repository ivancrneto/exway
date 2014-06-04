from rest_framework import serializers
from .models import Expense
import datetime


class ExpenseSerializer(serializers.ModelSerializer):

    date = serializers.DateField()
    time = serializers.TimeField()

    class Meta:
        model = Expense
        fields = ('id', 'description', 'amount', 'date', 'time', 'comment',
                  'created_on')
        read_only_fields = ('id', 'created_on')
