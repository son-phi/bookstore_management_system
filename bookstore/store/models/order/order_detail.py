from django.db import models

class OrderDetail(models.Model):
    detailID = models.AutoField(primary_key=True)
    orderID = models.ForeignKey("store.Order", on_delete=models.CASCADE, db_column="orderID")
    bookID = models.ForeignKey("store.Book", on_delete=models.CASCADE, db_column="bookID")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def getSubTotal(self):
        pass
