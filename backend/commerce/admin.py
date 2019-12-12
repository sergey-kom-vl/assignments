from django.contrib import admin

from .models import Point, Printer, Check


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    list_display = 'id', 'name',
    search_fields = 'name',
    ordering = 'name',


@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'check_type',
    search_fields = 'name',
    ordering = 'name',


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = 'id', 'type', 'printer_id', 'status',
    list_filter = 'type', 'printer_id', 'status'
    ordering = 'type', 'status',
