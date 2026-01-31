from django.db import models

class RecModel(models.Model):
    modelID = models.AutoField(primary_key=True)
    version = models.CharField(max_length=50)
    lastTrained = models.DateTimeField()
    algorithm = models.CharField(max_length=100)

    def trainModel(self):
        pass

    def deploy(self):
        pass
