from django.db import models

class WishlistItem(models.Model):
    itemID = models.AutoField(primary_key=True)
    wishlistID = models.ForeignKey("store.Wishlist", on_delete=models.CASCADE, db_column="wishlistID")
    bookID = models.ForeignKey("store.Book", on_delete=models.CASCADE, db_column="bookID")
    createdAt = models.DateTimeField()

    def addItem(self):
        pass

    def removeItem(self):
        pass
