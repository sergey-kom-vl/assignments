from django.db.models import Q
from django.http import JsonResponse, FileResponse
from rest_framework import viewsets

from .enums import CheckEnum
from .models import Check, Printer
from .permissions import PrinterApiPermission


class BaseApiViewSet(viewsets.ViewSet):
    permission_classes = PrinterApiPermission,

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if response.status_code == 403:
            return JsonResponse({"error": "Ошибка авторизации"}, status=401)
        return response


class CheckCreateViewSet(viewsets.ModelViewSet):
    permission_classes = ()
    authentication_classes = ()

    def create(self, request, *args, **kwargs):
        printers = Printer.objects.filter(point_id=request.data["point_id"])

        error_message = Printer.is_printout_checks_for_order(printers, order_id=int(request.data["id"]))
        if error_message != "":
            return JsonResponse({"error": error_message}, status=400)

        Printer.create_checks(printers, order_data=request.data)
        return JsonResponse({"ok": "Чеки успешно созданы"})


class NewCheckViewSet(BaseApiViewSet):
    queryset = Check.objects.filter(~Q(status=CheckEnum.STATUS_NEW))

    def list(self, request, *args, **kwargs):
        checks = [{"id": check.id} for check in self.queryset.filter(printer_id__api_key=request.GET["api_key"])]
        return JsonResponse({"checks": checks})


class CheckFileViewSet(BaseApiViewSet):
    queryset = Printer.objects.all()

    def get_file(self, request, *args, **kwargs):
        current_printer = self.queryset.get(api_key=request.GET["api_key"])

        error_message = current_printer.there_is_check_file_to_print(request.GET["check_id"])
        if error_message != "":
            return JsonResponse({"error": error_message}, status=400)

        response_check = current_printer.checks.get(id=request.GET["check_id"])
        return FileResponse(response_check.get_file_for_print(), content_type='application/pdf')
