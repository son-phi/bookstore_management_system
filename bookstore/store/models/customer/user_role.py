from django.db import models

class UserRole(models.Model):
    id = models.AutoField(primary_key=True)
    userID = models.ForeignKey("store.User", on_delete=models.CASCADE, db_column="userID")
    roleID = models.ForeignKey("store.Role", on_delete=models.CASCADE, db_column="roleID")
    assignedDate = models.DateTimeField()

    def assignRole(self):
        pass

    def revokeRole(self):
        pass
