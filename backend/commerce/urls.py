from django.conf.urls import url

from .views import PointViewSet, PrinterViewSet, CheckViewSet

urlpatterns = [
    url('points/', PointViewSet.as_view({'get': 'list'})),
    url('printer/', PrinterViewSet.as_view({'get': 'list'})),
    url('check/', CheckViewSet.as_view({'get': 'list', 'post': 'create'})),
]
