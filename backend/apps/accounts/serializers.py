from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id", "public_code", "email", "first_name", "last_name",
            "phone", "city", "role", "status", "created_at",
        )
        read_only_fields = ("public_code", "created_at")


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "phone", "password")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.username = validated_data["email"]
        user.role = User.Role.CLIENT
        user.set_password(password)
        user.save()
        return user
