from django.db import models

class OrderStatus(models.Model):
    statusID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def getOrdersByStatus(self):
        pass

    def __str__(self):
        return self.name
