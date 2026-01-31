from django.db import models

class Supplier(models.Model):
    supplierID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=30)
    taxCode = models.CharField(max_length=50)

    def createContract(self):
        pass

    def getSupplyHistory(self):
        pass

    def __str__(self):
        return self.name
