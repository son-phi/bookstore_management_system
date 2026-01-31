from django.db import models

class StockEntry(models.Model):
    entryID = models.AutoField(primary_key=True)
    warehouseID = models.ForeignKey("store.Warehouse", on_delete=models.CASCADE, db_column="warehouseID")
    bookID = models.ForeignKey("store.Book", on_delete=models.CASCADE, db_column="bookID")
    quantity = models.IntegerField()

    def updateQuantity(self):
        pass

    def moveStock(self):
        pass
