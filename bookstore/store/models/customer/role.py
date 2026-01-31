from django.db import models

class Role(models.Model):
    roleID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def getPermissions(self):
        pass

    def updateRole(self):
        pass

    def __str__(self):
        return self.name
