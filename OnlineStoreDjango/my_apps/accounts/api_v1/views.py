from drf_spectacular.utils import extend_schema
from my_apps.accounts.models import User
from my_apps.shop.api_v1.permissions import AdminPermission, GuestUserPermission
from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    MyTokenObtainPairSerializer,
    PasswordChangeSerializer,
    RegistrationSerializer,
    UserUrlSerializer,
)


class MyTokenObtainPairView(TokenObtainPairView):
    """Custom clas for add user info in tocken response"""

    serializer_class = MyTokenObtainPairSerializer


@extend_schema(tags=["User"])
class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """
    API endpoint that allows users to be viewed.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserUrlSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        data = {"detail": "Deleted", "code": "deleted"}
        return Response(status=status.HTTP_204_NO_CONTENT, data=data)


@extend_schema(tags=["User"])
class CreateUserView(generics.CreateAPIView):
    """
    API endpoint that allows to create user.
    """

    permission_classes = [IsAuthenticated, GuestUserPermission]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            if self.validate_roles(request):
                return Response(
                    {"detail": "this user can't create another user with this role"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            serializer.save()
            user = User.objects.get(email=serializer.data["email"])
            data = serializer.data
            data["id"] = user.id
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def validate_roles(request):
        """
        Describe what user can create other user with role.
        Like "manager" can create only "auth_user"
        """
        rules = {
            "guest_user": ["auth_user"],
            "auth_user": [],
            "manager": ["auth_user"],
            "admin": ["auth_user", "manager", "admin"],
        }
        if request.data["role"] in rules[request.user.get_role_display()]:
            return

        return True


@extend_schema(tags=["User"])
class ChangePasswordView(APIView):
    """
    API endpoint that allows to change user password.
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        serializer = PasswordChangeSerializer(
            context={"request": request}, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


import os
import requests

import google_auth_oauthlib.flow


class GoogleAuth(APIView):
    def get(self, request):
        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            client_config={
                "web": {
                    "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                    "project_id": os.getenv("GOOGLE_PROJECT_ID"),
                    "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
                    "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    # "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                }
            },
            scopes=["https://www.googleapis.com/auth/userinfo.email"],
        )

        # Indicate where the API server will redirect the user after the user completes
        # the authorization flow. The redirect URI is required. The value must exactly
        # match one of the authorized redirect URIs for the OAuth 2.0 client, which you
        # configured in the API Console. If this value doesn't match an authorized URI,
        # you will get a 'redirect_uri_mismatch' error.
        BASE_URL = os.getenv("BASE_URL")
        print("redirect_uri:", f"{BASE_URL}/api/v1/accounts/google_mail")
        flow.redirect_uri = f"{BASE_URL}/api/v1/accounts/google_mail"

        # Generate URL for request to Google's OAuth 2.0 server.
        # Use kwargs to set optional request parameters.
        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type="offline",
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes="true",
        )

        #return redirect(authorization_url)
        return Response(data={"authorization_url": authorization_url})

class GoogleMail(APIView):
    def get(self, request):
        state = request.GET.get("state")
        code = request.GET.get("code")
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
            state=state,
        )
        BASE_URL = os.getenv("BASE_URL")
        flow.redirect_uri = f"{BASE_URL}/api/v1/accounts/google_mail"
        flow.fetch_token(code=code)

        credentials = flow.credentials
        credentials = {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes,
        }
        print(credentials)
        GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
        response = requests.get(GOOGLE_USER_INFO_URL, params={"access_token": credentials["token"]})
        response_dict = response.json()
        return Response({"email": response_dict["email"]})