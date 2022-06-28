from rest_framework import viewsets
from django.contrib.auth.models import User
from api.serializers import UserSerializer, RoomSerializer
from base.models import Room


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all().order_by("created")
    serializer_class = RoomSerializer
