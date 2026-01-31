from django.db import models

class BookImage(models.Model):
    imageID = models.AutoField(primary_key=True)
    bookID = models.ForeignKey("store.Book", on_delete=models.CASCADE, db_column="bookID")
    url = models.CharField(max_length=255)
    isThumbnail = models.BooleanField(default=False)

    def uploadImage(self):
        pass

    def setThumbnail(self):
        pass
