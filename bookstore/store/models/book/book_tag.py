from django.db import models

class BookTag(models.Model):
    id = models.AutoField(primary_key=True)
    bookID = models.ForeignKey("store.Book", on_delete=models.CASCADE, db_column="bookID")
    tagID = models.ForeignKey("store.Tag", on_delete=models.CASCADE, db_column="tagID")

    def addTag(self):
        pass

    def removeTag(self):
        pass
