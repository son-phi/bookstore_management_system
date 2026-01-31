from django.db import models

class ShippingRate(models.Model):
    rateID = models.AutoField(primary_key=True)
    carrierID = models.ForeignKey("store.Carrier", on_delete=models.CASCADE, db_column="carrierID")
    zone = models.CharField(max_length=100)
    minWeight = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def getRate(self):
        pass
