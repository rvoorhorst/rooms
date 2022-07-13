from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers
from api.views import UserViewSet, RoomViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'rooms',RoomViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('api/', include(router.urls,)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
