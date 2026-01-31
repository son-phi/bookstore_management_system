from django.db import models

class Coupon(models.Model):
    couponID = models.AutoField(primary_key=True)
    code = models.CharField(max_length=100)
    discountID = models.ForeignKey("store.Discount", on_delete=models.CASCADE, db_column="discountID")
    usageLimit = models.IntegerField()

    def validateCode(self):
        pass

    def applyCoupon(self):
        pass

    def __str__(self):
        return self.code
