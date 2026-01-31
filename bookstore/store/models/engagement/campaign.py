from django.db import models

class Campaign(models.Model):
    campaignID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=50)

    def trackPerformance(self):
        pass

    def __str__(self):
        return self.name
