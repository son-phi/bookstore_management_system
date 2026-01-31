from django.db import models

class RecResult(models.Model):
    resultID = models.AutoField(primary_key=True)
    userID = models.ForeignKey("store.User", on_delete=models.CASCADE, db_column="userID")
    bookListJSON = models.TextField()
    score = models.FloatField()

    def getTopRecommendations(self):
        pass
