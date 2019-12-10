from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

from . import settings

admin.site.site_header = 'Администрирование Assignments'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
