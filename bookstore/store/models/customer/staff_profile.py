from django.db import models

class StaffProfile(models.Model):
    profileID = models.AutoField(primary_key=True)
    userID = models.ForeignKey("store.User", on_delete=models.CASCADE, db_column="userID")
    employeeCode = models.CharField(max_length=50)
    department = models.CharField(max_length=100)

    def updateStatus(self):
        pass

    def getKPI(self):
        pass
