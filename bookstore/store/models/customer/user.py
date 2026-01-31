from django.db import models

class User(models.Model):
    userID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=30)
    lastLogin = models.DateTimeField(null=True, blank=True)
    isActive = models.BooleanField(default=True)

    def register(self):
        pass

    def login(self):
        pass

    def changePassword(self):
        pass

    def __str__(self):
        return self.username
