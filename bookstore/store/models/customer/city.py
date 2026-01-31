from django.db import models

class City(models.Model):
    cityID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)

    def getDistricts(self):
        pass

    def __str__(self):
        return self.name
