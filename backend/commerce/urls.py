from django.conf.urls import url

from .views import PointViewSet, PrinterViewSet, CheckViewSet, CheckCreateViewSet

urlpatterns = [
    url('points/', PointViewSet.as_view({'get': 'list'})),
    url('printer/', PrinterViewSet.as_view({'get': 'list'})),
    url('check/', CheckViewSet.as_view({'get': 'list'})),

    url('create_checks/', CheckCreateViewSet.as_view({'post': 'create'})),
]
