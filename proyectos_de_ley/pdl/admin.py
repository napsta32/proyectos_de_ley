from django.contrib import admin

from pdl.models import Proyecto


class ProyectoAdmin(admin.ModelAdmin):
    list_display = [
        'legislatura',
        'numero_proyecto',
        'codigo',
        'titulo',
        'congresistas',
    ]


admin.site.register(Proyecto, ProyectoAdmin)
