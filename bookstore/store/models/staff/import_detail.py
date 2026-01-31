from django.db import models

class ImportDetail(models.Model):
    id = models.AutoField(primary_key=True)
    slipID = models.ForeignKey("store.ImportSlip", on_delete=models.CASCADE, db_column="slipID")
    bookID = models.ForeignKey("store.Book", on_delete=models.CASCADE, db_column="bookID")
    quantity = models.IntegerField()
    costPrice = models.DecimalField(max_digits=10, decimal_places=2)

    def calculateLineTotal(self):
        pass
