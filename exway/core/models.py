""" Models for core app """

from django.db import models
from datetime import datetime


class Expense(models.Model):
    """ Expense model """
    description = models.CharField(max_length=256)
    datetime = models.DateTimeField()
    amount = models.DecimalField(decimal_places=2, max_digits=100)
    comment = models.CharField(max_length=100, null=True, blank=True)

    user = models.ForeignKey('auth.User', related_name='expenses')

    created_on = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super(Expense, self).__init__(*args, **kwargs)

        # in some situations the model is initialized using datetime and
        # in other ones, using a date and a time. For the second case, we need
        # to pick up the date and time arguments and set to the class
        date = kwargs.pop('date', False)
        if date:
            self.date = date
        time = kwargs.pop('time', False)
        if time:
            self.time = time

    # these date and time properties are needed because the model uses
    # datetime but the api separates in two fields: date and time.
    def get_date(self):
        """ Returns date part of datetime attribute """
        return self.datetime.date()

    def set_date(self, date):
        """ Sets date part of datetime attribute """
        if self.datetime:
            self.datetime = datetime.combine(date, self.datetime.time())
        else:
            self.datetime = datetime.combine(date, datetime.min.time())

    def get_time(self):
        """ Returns time part of datetime attribute """
        return self.datetime.time()

    def set_time(self, time):
        """ Sets time part of datetime attribute """
        if self.datetime:
            self.datetime = datetime.combine(self.datetime.date(), time)
        else:
            self.datetime = datetime.combine(datetime.min.date(), time)

    date = property(get_date, set_date)
    time = property(get_time, set_time)
