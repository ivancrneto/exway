from django.db import models

class Expense(models.Model):
    description = models.CharField(max_length=256)
    datetime = models.DateTimeField()
    amount = models.DecimalField(decimal_places=2, max_digits=100)
    comment = models.CharField(max_length=100)

    created_on = models.DateTimeField(auto_now_add=True)

    def get_date(self):
        return self.datetime.date()

    def set_date(self, date):
        self.datetime = datetime.datetime.combine(date, self.datetime.time())

    def get_time(self):
        return self.datetime.time()

    def set_time(self, time):
        self.datetime = datetime.datetime.combine(self.datetime.date(), time)

    date = property(get_date, set_date)
    time = property(get_time, set_time)
