from django.db import models

class Language(models.Model):
    langID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)

    def filterByLang(self):
        pass
