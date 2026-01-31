from django.db import models

class ShippingTrace(models.Model):
    traceID = models.AutoField(primary_key=True)
    shipmentID = models.ForeignKey("store.Shipment", on_delete=models.CASCADE, db_column="shipmentID")
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    time = models.DateTimeField()

    def addTraceLog(self):
        pass
