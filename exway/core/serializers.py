from rest_framework import serializers
from .models import Expense


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
        super(ExpenseSerializer, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.object.user = self.request.user
        super(ExpenseSerializer, self).save(*args, **kwargs)
