from django.http import JsonResponse
from rest_framework import viewsets

from .models import Point, Printer, Check
from .serializers import PointSerializer, PrinterSerializer, CheckSerializer, CheckCreateFormSerializer


class PointViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Point.objects.all()
    serializer_class = PointSerializer


class PrinterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer


class CheckViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer


class CheckCreateViewSet(viewsets.ModelViewSet):
    serializer_class = CheckCreateFormSerializer
    permission_classes = ()
    authentication_classes = ()

    def create(self, request, *args, **kwargs):
        current_point = Point.objects.get(id=request.data["point_id"])

        error_message = current_point.is_printout_checks_for_order(order_id=request.data["id"])
        if error_message != "":
            return JsonResponse({"error": error_message}, status=400)

        current_point.create_checks(order_data=request.data)
        return JsonResponse({"ok": "Чеки успешно созданы"})
