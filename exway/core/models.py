from django.db import models

class Expense(models.Model):
    description = models.CharField(max_length=256)
    datetime = models.DateTimeField()
    amount = models.DecimalField(decimal_places=2, max_digits=100)
    comment = models.CharField(max_length=100)

    created_on = models.DateTimeField(auto_now_add=True)
