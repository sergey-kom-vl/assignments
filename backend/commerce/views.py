from django.http import JsonResponse
from rest_framework import viewsets

from .enums import CheckEnum
from .models import Point, Check
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
        current_point = Point.objects.get(id=request.data["point_id"])

        error_message = current_point.is_printout_checks_for_order(order_id=request.data["id"])
        if error_message != "":
            return JsonResponse({"error": error_message}, status=400)

        current_point.create_checks(order_data=request.data)
        return JsonResponse({"ok": "Чеки успешно созданы"})


class NewCheckViewSet(BaseApiViewSet):
    queryset = Check.objects.filter(status=CheckEnum.STATUS_NEW)

    def list(self, request, *args, **kwargs):
        checks = [{"id": check.id} for check in self.queryset.filter(printer_id__api_key=request.GET["api_key"])]
        return JsonResponse({"checks": checks})
