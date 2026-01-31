from django.db import models

class UserCoupon(models.Model):
    id = models.AutoField(primary_key=True)
    userID = models.ForeignKey("store.User", on_delete=models.CASCADE, db_column="userID")
    couponID = models.ForeignKey("store.Coupon", on_delete=models.CASCADE, db_column="couponID")
    isUsed = models.BooleanField(default=False)

    def markAsUsed(self):
        pass
