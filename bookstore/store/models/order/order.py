from django.db import models

class Order(models.Model):
    orderID = models.AutoField(primary_key=True)
    userID = models.ForeignKey("store.User", on_delete=models.CASCADE, db_column="userID")
    totalAmount = models.DecimalField(max_digits=12, decimal_places=2)
    shippingFee = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField()

    def placeOrder(self):
        pass

    def cancelOrder(self):
        pass
