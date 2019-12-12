from rest_framework import permissions

from .models import Printer


class PrinterApiPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        printer = Printer.objects.filter(api_key=request.GET["api_key"]).exists()
        return printer
