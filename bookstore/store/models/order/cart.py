from django.db import models

class Cart(models.Model):
    cartID = models.AutoField(primary_key=True)
    userID = models.ForeignKey("store.User", null=True, blank=True, on_delete=models.SET_NULL, db_column="userID")
    sessionKey = models.CharField(max_length=255)
    updatedAt = models.DateTimeField()

    def clearCart(self):
        pass

    def getCartTotal(self):
        pass
