from django.db import models

class Wishlist(models.Model):
    wishlistID = models.AutoField(primary_key=True)
    userID = models.ForeignKey("store.User", on_delete=models.CASCADE, db_column="userID")
    name = models.CharField(max_length=200)

    def shareWishlist(self):
        pass
