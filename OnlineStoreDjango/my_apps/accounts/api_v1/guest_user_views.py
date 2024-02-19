from django.core.mail import send_mail
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from OnlineStoreDjango import settings
from my_apps.accounts.models import User
from my_apps.shop.api_v1.permissions import AdminPermission, GuestUserPermission
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


from rest_framework import serializers

from my_apps.accounts.models import User

EMAIL = """
We wanted to extend our warmest gratitude to you for choosing GiftHub and completing the registration process. 
Welcome to our community! We're thrilled to have you on board.
Your registration is the first step in an exciting journey, 
and we are committed to making your experience with us remarkable. 
By joining our platform, you gain access to a world of possibilities, 
and we can't wait to show you all that we have to offer."""


class CreateUserView(APIView):
    """
    API endpoint that allows to create auth_user.
    """

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

    class RegisterAuthUserWithToken(serializers.ModelSerializer):
        access = serializers.CharField()
        refresh = serializers.CharField()

        class Meta:
            model = User
            fields = ["email", "password", "refresh", "access"]
            extra_kwargs = {"password": {"write_only": True}}

    @extend_schema(
        tags=["Guest_user"],
        request=RegisterAuthUser,
        responses=RegisterAuthUserWithToken,
        # more customizations
    )
    def post(self, request):
        serializer = self.RegisterAuthUser(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(email=serializer.data["email"])
            send_mail(
                subject="Registration on the GiftHub",
                message=f"Dear {user.get_full_name()} \n " + EMAIL,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
            data = serializer.data
            data["id"] = user.id
            refresh = RefreshToken.for_user(user)
            data["access"] = str(refresh.access_token)
            data["refresh"] = str(refresh)
            response = Response(data, status=status.HTTP_201_CREATED)
            response.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                value=data["access"],
                domain=settings.SIMPLE_JWT["AUTH_COOKIE_DOMAIN"],
                path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
                expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
