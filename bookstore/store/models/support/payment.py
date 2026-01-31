from django.db import models

class Payment(models.Model):
    paymentID = models.AutoField(primary_key=True)
    orderID = models.ForeignKey("store.Order", on_delete=models.CASCADE, db_column="orderID")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=50)
    method = models.CharField(max_length=50)

    def processPayment(self):
        pass

    def refund(self):
        pass

