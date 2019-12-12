from django.conf.urls import url

from .views import NewCheckViewSet, CheckCreateViewSet, CheckFileViewSet

urlpatterns = [
    url('create_checks/', CheckCreateViewSet.as_view({'post': 'create'})),
    url('new_check/', NewCheckViewSet.as_view({'get': 'list'})),
    url('check/', CheckFileViewSet.as_view({'get': 'get_file'})),
]
