from rest_framework import serializers
from django.contrib.auth.models import User
from base.models import Room


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "is_staff"]


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["host", "topic", "name", "description", "updated", "created"]

