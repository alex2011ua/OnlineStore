from my_apps.accounts.models import User
from django.contrib.auth.models import Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'email', 'first_name', 'middle_name', 'last_name', 'address', 'dob', 'gender', 'role', 'notice', "get_age"]
