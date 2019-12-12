from django.contrib import admin

from .models import Printer, Check


@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'check_type', 'api_key',
    search_fields = 'name',
    ordering = 'name',


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = 'id', 'type', 'printer_id', 'status',
    list_filter = 'type', 'printer_id', 'status'
    ordering = 'type', 'status',
