from rest_framework import viewsets

from .models import Point, Printer, Check
from .serializers import PointSerializer, PrinterSerializer, CheckSerializer


class PointViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Point.objects.all()
    serializer_class = PointSerializer


class PrinterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer


class CheckViewSet(viewsets.ModelViewSet):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
