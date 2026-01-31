from django.db import models

class Transaction(models.Model):
    transID = models.AutoField(primary_key=True)
    paymentID = models.ForeignKey("store.Payment", on_delete=models.CASCADE, db_column="paymentID")
    gatewayRef = models.CharField(max_length=255)
    timestamp = models.DateTimeField()

    def logTransaction(self):
        pass

    def verify(self):
        pass
