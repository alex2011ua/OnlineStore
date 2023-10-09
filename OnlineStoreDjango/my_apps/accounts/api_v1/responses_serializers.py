from rest_framework import serializers

from my_apps.accounts.models import User


class RegisterAuthUserWithToken(serializers.ModelSerializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    class Meta:
        model = User
        fields = ["email", "password", "refresh", "access"]
        extra_kwargs = {"password": {"write_only": True}}
