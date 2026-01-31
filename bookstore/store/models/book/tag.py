from django.db import models

class Tag(models.Model):
    tagID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    colorCode = models.CharField(max_length=20)

    def getRelatedBooks(self):
        pass

    def __str__(self):
        return self.name
