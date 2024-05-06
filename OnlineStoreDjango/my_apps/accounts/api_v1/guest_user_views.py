from django.core.mail import send_mail
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from OnlineStoreDjango import settings
from my_apps.shop.api_v1.permissions import AdminPermission, GuestUserPermission
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


from rest_framework import serializers

from my_apps.accounts.models import User
from .utils import create_user
from django.core.mail import send_mail
from django.shortcuts import render
from my_apps.accounts.models import User
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
import os
import requests
from .utils import get_user_by_email, create_user, get_tokens_for_user
import google_auth_oauthlib.flow
from rest_framework.exceptions import NotFound

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
        serializer.is_valid(raise_exception=True)

        user = create_user(**serializer.validated_data)

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


SCOPES = [
    "email",
    "profile",
    "openid",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
]


class GoogleAuthURL(APIView):
    class OutputGoogleAuthURLSerializer(serializers.Serializer):
        authorization_url = serializers.CharField(max_length=1000)

    def get(self, request):
        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            client_config={
                "web": {
                    "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                    "project_id": os.getenv("GOOGLE_PROJECT_ID"),
                    "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
                    "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                }
            },
            scopes=SCOPES,
        )

        BASE_URL = os.getenv("BASE_URL")
        print("redirect_uri:", f"{BASE_URL}api/v1/accounts/google_auth")
        flow.redirect_uri = f"{BASE_URL}api/v1/accounts/google_auth"
        authorization_url, state = flow.authorization_url()

        return Response(data={"authorization_url": authorization_url})


class GoogleAuth(APIView):
    class InputGoogleAuthSerializer(serializers.Serializer):
        # state = serializers.CharField(max_length=1000, required=False)
        code = serializers.CharField(max_length=1000)

    def get(self, request):
        code = request.GET.get("code")
        return Response(data={"code": code})


class GoogleAuthCode(APIView):
    class InputGoogleAuthSerializer(serializers.Serializer):
        code = serializers.CharField(max_length=1000)
        redirect_uri = serializers.CharField(max_length=1000, required=False)

    class OutputGoogleAuthSerializer(serializers.Serializer):
        first_name = serializers.CharField(max_length=150)
        last_name = serializers.CharField(max_length=150)
        email = serializers.EmailField()
        token = serializers.CharField(max_length=150)

    @extend_schema(
        summary="Change code to authenticate user.",
        tags=["Accounts"],
        request=InputGoogleAuthSerializer,
        responses=OutputGoogleAuthSerializer,
    )
    def post(self, request):
        serializer = self.InputGoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data["code"]
        redirect_uri = serializer.validated_data.get("redirect_uri")

        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            client_config={
                "web": {
                    "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                    "project_id": os.getenv("GOOGLE_PROJECT_ID"),
                    "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
                    "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                }
            },
            scopes=None,
            state=None,
        )

        if redirect_uri:
            flow.redirect_uri = redirect_uri
        else:
            flow.redirect_uri = "postmessage"
            # BASE_URL = os.getenv("BASE_URL")
            # flow.redirect_uri = f"{BASE_URL}api/v1/accounts/google_auth"
        # get token from code
        try:
            access_credentials_payload = flow.fetch_token(code=code)
        except Exception as e:
            detail = {
                "code": code,
                "redirect_uri": flow.redirect_uri,
            }
            return Response(
                data={"error": str(e), "detail": detail}, status=status.HTTP_400_BAD_REQUEST
            )

        credentials = flow.credentials
        credentials = {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes,
        }
        GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
        response = requests.get(GOOGLE_USER_INFO_URL, params={"access_token": credentials["token"]})
        response_dict = response.json()
        """{
        'sub': '11516534...', 
        'name': 'Oleksii...', 
        'given_name': 'Oleksii...', 
        'picture': 'https://lh3.googleusercontent.com/a/...', 
        'email': 'oleksii...@gmail.com', 
        'email_verified': True, 
        'locale': 'uk'

        'name': 'Oleksii...', 
        'given_name': 'Oleksii...', 
        'family_name': 'Kovalenko...',
        }"""
        try:
            user = get_user_by_email(response_dict["email"])
        except NotFound:
            user = create_user(
                response_dict["email"],
                "some_password",
                first_name=response_dict.get("given_name", None),
                last_name=response_dict.get("family_name", None),
            )
        token = get_tokens_for_user(user)

        return Response(
            data={
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.get_role_display(),
                "email": user.email,
                "access": token.get("access"),
                "refresh": token.get("refresh"),
            }
        )

class FacebookAuthCode(APIView):
    class InputFacebookAuthSerializer(serializers.Serializer):
        code = serializers.CharField(max_length=1000)
        redirect_uri = serializers.CharField(max_length=1000, required=False)

    class OutputFacebookAuthSerializer(serializers.Serializer):
        first_name = serializers.CharField(max_length=150)
        last_name = serializers.CharField(max_length=150)
        email = serializers.EmailField()
        token = serializers.CharField(max_length=150)

    def get(self, request):
        code = request.GET.get("code")
        print(code)
        return Response(data={"code": code})

    @extend_schema(
        summary="Change code to authenticate user.",
        tags=["Accounts"],
        request=InputFacebookAuthSerializer,
        responses=OutputFacebookAuthSerializer,
    )
    def post(self, request):
        def get_user_data(access_token):
            user_url = 'https://graph.facebook.com/v19.0/me'
            params = {'access_token': access_token, 'fields': 'id,name,email,first_name,last_name'}
            response = requests.get(user_url, params=params)
            if response.ok:
                return response.json()
            else:
                raise Exception("Ошибка получения данных пользователя")

        serializer = self.InputFacebookAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data["code"]
        redirect_uri = serializer.validated_data.get("redirect_uri")
        token_url = 'https://graph.facebook.com/v19.0/oauth/access_token'
        payload = {
            'client_id': os.getenv("FACEBOOK_ID"),
            'client_secret': os.getenv("FACEBOOK_SECRET"),
            'code': code,
            'redirect_uri': redirect_uri
        }
        response = requests.get(token_url, params=payload)
        if response.ok:
            return response.json()  # Возвращает объект с токеном доступа и другими данными
        else:
            raise Exception(f"Ошибка при обмене кода авторизации: {response.text}")


from django.shortcuts import render

def facebook(request):
    return render(request, "oauth/facebook_start.html")