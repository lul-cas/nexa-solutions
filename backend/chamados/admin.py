from django.contrib import admin

from .models import Chamado


@admin.register(Chamado)
class ChamadoAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "status", "criado_em")
    list_filter = ("status",)
    search_fields = ("titulo", "descricao")
