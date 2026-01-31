from django.db import models

class UserBehavior(models.Model):
    id = models.AutoField(primary_key=True)
    userID = models.ForeignKey("store.User", on_delete=models.CASCADE, db_column="userID")
    bookID = models.ForeignKey("store.Book", on_delete=models.CASCADE, db_column="bookID")
    actionType = models.CharField(max_length=50)
    timestamp = models.DateTimeField()

    def logAction(self):
        pass
