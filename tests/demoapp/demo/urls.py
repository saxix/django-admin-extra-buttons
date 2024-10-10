from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

admin.autodiscover()

urlpatterns = [
    path(r'admin/', admin.site.urls),
] + staticfiles_urlpatterns()
