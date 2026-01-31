from django.db import models

class CustomerProfile(models.Model):
    profileID = models.AutoField(primary_key=True)
    userID = models.ForeignKey("store.User", on_delete=models.CASCADE, db_column="userID")
    avatar = models.CharField(max_length=255)
    loyaltyPoints = models.IntegerField()
    dob = models.DateField()

    def updateProfile(self):
        pass

    def getLoyaltyLevel(self):
        pass
