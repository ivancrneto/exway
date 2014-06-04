from rest_framework import serializers
from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense
        fields = ('id', 'description', 'datetime', 'amount', 'comment',
                  'created_on')
        read_only_fields = ('id', 'created_on')
