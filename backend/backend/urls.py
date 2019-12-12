from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from . import settings

admin.site.site_header = 'Администрирование Assignments'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),

    url(r'', include('commerce.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
