from django.db import models

class OrderHistory(models.Model):
    historyID = models.AutoField(primary_key=True)
    orderID = models.ForeignKey("store.Order", on_delete=models.CASCADE, db_column="orderID")
    statusID = models.ForeignKey("store.OrderStatus", on_delete=models.CASCADE, db_column="statusID")
    changedBy = models.ForeignKey("store.User", on_delete=models.CASCADE, db_column="changedBy")
    changedAt = models.DateTimeField()

    def logStatusChange(self):
        pass
