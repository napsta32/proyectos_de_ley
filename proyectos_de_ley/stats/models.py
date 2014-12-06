from django.db import models


class ComisionCount(models.Model):
    count = models.IntegerField()
    comision = models.CharField(max_length=250)
