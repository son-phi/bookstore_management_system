from django.db import models

class Permission(models.Model):
    permissionID = models.AutoField(primary_key=True)
    codeName = models.CharField(max_length=100)
    description = models.TextField()

    def checkPermission(self):
        pass

    def __str__(self):
        return self.codeName
