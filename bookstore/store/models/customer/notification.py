from django.db import models

class Notification(models.Model):
    notiID = models.AutoField(primary_key=True)
    userID = models.ForeignKey("store.User", on_delete=models.CASCADE, db_column="userID")
    title = models.CharField(max_length=200)
    content = models.TextField()
    isRead = models.BooleanField(default=False)

    def markAsRead(self):
        pass

    def sendPush(self):
        pass
