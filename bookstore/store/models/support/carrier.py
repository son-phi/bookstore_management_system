from django.db import models

class Carrier(models.Model):
    carrierID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    apiKey = models.CharField(max_length=255)
    hotline = models.CharField(max_length=30)

    def calculateShippingFee(self):
        pass

    def __str__(self):
        return self.name
