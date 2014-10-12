from django.db import models


# Create your models here.
class Iniciativas(models.Model):
    nodes = models.TextField(blank=True)
    links = models.TextField(blank=True)
