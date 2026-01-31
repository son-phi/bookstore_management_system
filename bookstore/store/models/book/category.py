from django.db import models

class Category(models.Model):
    categoryID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    parentID = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, db_column="parentID"
    )

    def getChildren(self):
        pass

    def getBooks(self):
        pass

    def __str__(self):
        return self.name
