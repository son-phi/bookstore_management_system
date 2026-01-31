from django.db import models

class Warehouse(models.Model):
    warehouseID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=255)
    capacity = models.IntegerField()

    def checkCapacity(self):
        pass

    def manageStock(self):
        pass

    def __str__(self):
        return self.name
