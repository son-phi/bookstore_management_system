from django.db import models

class Address(models.Model):
    addressID = models.AutoField(primary_key=True)
    userID = models.ForeignKey("store.User", on_delete=models.CASCADE, db_column="userID")
    street = models.CharField(max_length=255)
    districtID = models.ForeignKey("store.District", on_delete=models.CASCADE, db_column="districtID", null=True)
    isDefault = models.BooleanField(default=False)

    def createAddress(self):
        pass

    def deleteAddress(self):
        pass
