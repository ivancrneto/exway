""" Module for API serializers classes """

from rest_framework import serializers
from .models import Expense
import time


class ExpenseSerializer(serializers.ModelSerializer):
    """ Serializer class for Expense model """

    date = serializers.DateField()
    time = serializers.TimeField()
    user = serializers.Field(source='user.username')

    class Meta:
        """ Meta class for ExpenseSerializer """
        model = Expense
        fields = ('id', 'description', 'amount', 'date', 'time', 'comment',
                  'created_on', 'user')
        read_only_fields = ('id', 'created_on')

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        if 'data' in kwargs and 'time' in kwargs['data']:
            kwargs['data']['time'] = time.strptime(kwargs['data']['time'],
                                                   '%I:%M %p')
            kwargs['data']['time'] = time.strftime('%H:%M',
                                                   kwargs['data']['time'])
        super(ExpenseSerializer, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        """ Handles expense save from serialized data """
        self.object.user = self.request.user
        super(ExpenseSerializer, self).save(*args, **kwargs)
