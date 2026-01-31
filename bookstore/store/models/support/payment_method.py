from django.db import models

class PaymentMethod(models.Model):
    methodID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    configJSON = models.TextField()
    isActive = models.BooleanField(default=True)

    def validateMethod(self):
        pass

    def __str__(self):
        return self.name
