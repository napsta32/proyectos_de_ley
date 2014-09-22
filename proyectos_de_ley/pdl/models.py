from django.db import models


# Create your models here.
class Proyecto(models.Model):
    codigo = models.CharField(max_length=20)
    numero_proyecto = models.CharField(max_length=50)
    short_url = models.CharField(max_length=20)
    congresistas = models.TextField(blank=True)

    # migrate from date as string
    fecha_presentacion = models.DateField(blank=True)
    titulo = models.TextField(blank=True)
    expediente = models.URLField(max_length=200, blank=True)
    pdf_url = models.URLField(max_length=200, blank=True)
    seguimiento_page = models.URLField(max_length=200, blank=True)

    # migrate from timestamp field
    time_created = models.DateTimeField(auto_now_add=True)
    time_edited = models.DateTimeField(auto_now=True)

    # > v1.1.1
    proponente = models.CharField(max_length=250, blank=True, default='')
    grupo_parlamentario = models.CharField(max_length=250, blank=True,
                                           default='')
    iniciativas_agrupadas = models.TextField(blank=True, default='')
    nombre_comision = models.CharField(max_length=250, blank=True, default='')
    titulo_de_ley = models.TextField(blank=True, default='')
    numero_de_ley = models.CharField(max_length=200, blank=True, default='')


class Slug(models.Model):
    """A translation table between a Congresista name and a slug to be used
    as hiperlink."""
    nombre = models.CharField(max_length=200)
    slug = models.CharField(max_length=100)
