from django.db import models

class Publisher(models.Model):
    publisherID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=255)
    website = models.CharField(max_length=255)

    def getBooksByPublisher(self):
        pass

    def __str__(self):
        return self.name
