from django.db import models

class Review(models.Model):
    reviewID = models.AutoField(primary_key=True)
    userID = models.ForeignKey("store.User", on_delete=models.CASCADE, db_column="userID")
    bookID = models.ForeignKey("store.Book", on_delete=models.CASCADE, db_column="bookID")
    rating = models.IntegerField()
    comment = models.TextField()

    def postReview(self):
        pass

    def editReview(self):
        pass
