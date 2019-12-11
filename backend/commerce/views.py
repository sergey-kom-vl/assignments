from django_rq import enqueue as rq_enqueue
from rest_framework import viewsets

from .models import Point, Printer, Check
from .tasks import generate_check_file
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
        response = super().create(request, *args, **kwargs)
        rq_enqueue(generate_check_file, response.data)
        # generate_check_file(response.data)
        # rq_enqueue(generate_pdf_for_check, data)

        return response
