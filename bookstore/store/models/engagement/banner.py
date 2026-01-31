from django.db import models

class Banner(models.Model):
    bannerID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    imageUrl = models.CharField(max_length=255)
    linkUrl = models.CharField(max_length=255)
    position = models.CharField(max_length=50)
    isActive = models.BooleanField(default=True)

    def toggleVisibility(self):
        pass

    def __str__(self):
        return self.title
