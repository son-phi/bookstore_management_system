from django.db import models

class SystemConfig(models.Model):
    configID = models.AutoField(primary_key=True)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=255)
    description = models.TextField()

    def getConfig(self):
        pass

    def setConfig(self):
        pass

    def __str__(self):
        return self.key
