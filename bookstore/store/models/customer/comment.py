from django.db import models

class Comment(models.Model):
    commentID = models.AutoField(primary_key=True)
    userID = models.ForeignKey("store.User", on_delete=models.CASCADE, db_column="userID")
    bookID = models.ForeignKey("store.Book", on_delete=models.CASCADE, db_column="bookID")
    parentID = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, db_column="parentID")
    content = models.TextField()

    def replyComment(self):
        pass

    def delete(self):
        pass
