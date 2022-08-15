from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name")
        read_only_fields = ("id", "username", "first_name", "last_name")


class UserDetailSerializer(UserSerializer):
    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + ("email",)
        read_only_fields = ("id", "username")
