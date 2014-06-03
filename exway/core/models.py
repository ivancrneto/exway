from django.db import models

class Expense(models.Model):
    description = models.CharField(max_length=256)
    datetime = models.DatetimeField()
    amount = models.DecimalField()
    comment = models.CharField(max_length=100)

    created_on = models.DatetimeField(auto_now_add=True)
