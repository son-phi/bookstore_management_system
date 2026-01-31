from django.db import models

class ReturnRequest(models.Model):
    returnID = models.AutoField(primary_key=True)
    orderID = models.ForeignKey("store.Order", on_delete=models.CASCADE, db_column="orderID")
    reason = models.TextField()
    status = models.CharField(max_length=50)
    refundAmount = models.DecimalField(max_digits=12, decimal_places=2)

    def approveReturn(self):
        pass

    def rejectReturn(self):
        pass

