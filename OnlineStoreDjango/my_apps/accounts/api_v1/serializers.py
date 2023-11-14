from my_apps.accounts.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from my_apps.shop.models import Order


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Add some info about user in token response"""

    def validate(self, attrs):
        data = super().validate(attrs)
        data["id"] = self.user.pk
        data["email"] = self.user.email
        data["role"] = self.user.get_role_display()
        data["mobile"] = self.user.mobile
        data["full_name"] = self.user.get_full_name()
        data["first_name"] = self.user.first_name
        data["middle_name"] = self.user.middle_name
        data["last_name"] = self.user.last_name

        data["address"] = self.user.address
        data["dob"] = self.user.dob
        data["age"] = self.user.get_age()

        data["gender"] = self.user.get_gender_display()
        data["notice"] = self.user.notice

        data["created_at"] = self.user.created_at
        data["updated_at"] = self.user.updated_at
        order = Order.get_current_order_id(self.user)
        data["order"] = order.id
        return data


class UserUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = [
            "id",
            "url",
            "email",
            "first_name",
            "middle_name",
            "last_name",
            "address",
            "dob",
            "gender",
            "role",
            "notice",
            "get_age",
        ]

    gender = serializers.CharField(source="get_gender_display")
    role = serializers.CharField(source="get_role_display")


class RegistrationSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="get_role_display")

    def validate_role(self, value):
        ROLE_CHOICES = {
            "admin": "A",
            "manager": "M",
            "auth_user": "U",
            "guest_user": "G",
        }
        if value in ROLE_CHOICES:
            return ROLE_CHOICES[value]
        else:
            raise serializers.ValidationError({"detail": "wrong role field"})

    class Meta:
        model = User
        fields = ["email", "password", "role"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
       password=validated_data.pop('password',None)
       instance=self.Meta.model(**validated_data)
       if password is not None:
           instance.set_password(password)
       instance.save()
       return instance


    def save(self):
        user = User(
            email=self.validated_data["email"],
            role=self.validated_data["get_role_display"],
        )
        password = self.validated_data["password"]

        user.set_password(password)
        user.save()
        return user


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        style={"input_type": "password"}, required=True
    )
    new_password = serializers.CharField(
        style={"input_type": "password"}, required=True
    )

    def validate_current_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError({"current_password": "Does not match"})
        return value


class RegisterAuthUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        user = User(
            email=self.validated_data["email"],
        )
        password = self.validated_data["password"]
        user.set_password(password)
        user.first_name = self.validated_data["first_name"]
        user.last_name = self.validated_data["last_name"]
        user.save()
        return user

