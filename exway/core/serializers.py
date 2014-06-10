from rest_framework import serializers
from .models import Expense
import time


class ExpenseSerializer(serializers.ModelSerializer):

    date = serializers.DateField()
    time = serializers.TimeField()
    user = serializers.Field(source='user.username')

    class Meta:
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
        self.object.user = self.request.user
        super(ExpenseSerializer, self).save(*args, **kwargs)
