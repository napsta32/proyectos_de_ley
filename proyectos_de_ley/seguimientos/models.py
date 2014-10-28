from django.db import models


# Create your models here.
class Iniciativas(models.Model):
    nodes = models.TextField(blank=True)
    links = models.TextField(blank=True)


class SeguimientosJson(models.Model):
    headline = models.TextField(blank=True)
    codigo = models.TextField(blank=True)
    date = models.TextField(blank=True)
    type = models.TextField(blank=True)
    text = models.TextField(blank=True)
