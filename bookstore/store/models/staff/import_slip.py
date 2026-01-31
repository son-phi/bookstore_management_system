from django.db import models

class ImportSlip(models.Model):
    slipID = models.AutoField(primary_key=True)
    warehouseID = models.ForeignKey("store.Warehouse", on_delete=models.CASCADE, db_column="warehouseID")
    supplierID = models.ForeignKey("store.Supplier", on_delete=models.CASCADE, db_column="supplierID")
    staffID = models.ForeignKey("store.User", on_delete=models.CASCADE, db_column="staffID")
    totalCost = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, default="PENDING")

    def createSlip(self):
        pass

    def approveSlip(self):
        pass
