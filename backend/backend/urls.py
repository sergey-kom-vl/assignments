from django.conf.urls import url
from django.contrib import admin

admin.site.site_header = 'Администрирование Assignments'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
