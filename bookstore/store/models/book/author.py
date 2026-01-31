from django.db import models

class Author(models.Model):
    authorID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    bio = models.TextField()
    photoUrl = models.CharField(max_length=255)

    def getBooksByAuthor(self):
        pass

    def __str__(self):
        return self.name
