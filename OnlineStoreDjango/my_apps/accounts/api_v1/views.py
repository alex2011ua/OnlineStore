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

