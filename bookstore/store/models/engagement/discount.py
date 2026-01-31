from django.db import models

class Discount(models.Model):
    discountID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=50)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()

    def isValid(self):
        pass

    def __str__(self):
        return self.name
