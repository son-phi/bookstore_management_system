from django.db import models

class Book(models.Model):
    bookID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    description = models.TextField()
    categoryID = models.ForeignKey("store.Category", null=True, blank=True, on_delete=models.SET_NULL, db_column="categoryID")

    def getDetail(self):
        pass

    def updateStock(self):
        pass

    def __str__(self):
        return self.title
