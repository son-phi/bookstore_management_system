from django.db import models

class BookAuthor(models.Model):
    id = models.AutoField(primary_key=True)
    bookID = models.ForeignKey("store.Book", on_delete=models.CASCADE, db_column="bookID")
    authorID = models.ForeignKey("store.Author", on_delete=models.CASCADE, db_column="authorID")
    role = models.CharField(max_length=100)

    def linkAuthor(self):
        pass
