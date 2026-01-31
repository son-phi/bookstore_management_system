from django.db import models

class Shipment(models.Model):
    shipmentID = models.AutoField(primary_key=True)
    orderID = models.ForeignKey("store.Order", on_delete=models.CASCADE, db_column="orderID")
    trackingCode = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    def createLabel(self):
        pass

    def updateTracking(self):
        pass
