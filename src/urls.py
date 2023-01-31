from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.base.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]
