from django.db import models

class CartItem(models.Model):
    itemID = models.AutoField(primary_key=True)
    cartID = models.ForeignKey("store.Cart", on_delete=models.CASCADE, db_column="cartID")
    bookID = models.ForeignKey("store.Book", on_delete=models.CASCADE, db_column="bookID")
    quantity = models.IntegerField()

    def updateQty(self):
        pass

    def removeItem(self):
        pass
