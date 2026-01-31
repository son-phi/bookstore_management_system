from django.db import models

class District(models.Model):
    districtID = models.AutoField(primary_key=True)
    cityID = models.ForeignKey("store.City", on_delete=models.CASCADE, db_column="cityID")
    name = models.CharField(max_length=100)

    def getWards(self):
        pass

    def __str__(self):
        return self.name
