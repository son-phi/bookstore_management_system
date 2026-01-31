from django.db import models

class ReviewImage(models.Model):
    imgID = models.AutoField(primary_key=True)
    reviewID = models.ForeignKey("store.Review", on_delete=models.CASCADE, db_column="reviewID")
    url = models.CharField(max_length=255)

    def uploadReviewImage(self):
        pass
