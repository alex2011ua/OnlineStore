from datetime import date
from typing import Any

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **other):
        """Create user.

        Returns:
            user: new user

        """
        user = self.model(
            email=self.normalize_email(email),
            password=password,
            **other,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create superuser.

        Returns:
            user: new superuser

        """
        return self.create_user(
            first_name="Alex",
            last_name="Kov",
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True,
        )


class User(AbstractUser):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    ROLE_CHOICES = [
        ('A', 'Admin'),
        ('M', 'Manager'),
        ('U', 'User'),
    ]
    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: list[str] = []

    first_name = models.CharField(_("first name"),blank=True, null=True, max_length=100)
    middle_name = models.CharField(_("middle name"),blank=True, null=True, max_length=100)
    last_name = models.CharField(_("last name"),blank=True, null=True, max_length=100)

    email = models.EmailField(_("email address"), unique=True)
    mobile = models.IntegerField(_("mobile phone"),blank=True, null=True)

    address = models.CharField(_("delivery address"), max_length=255, blank=True)
    dob = models.DateField(_("Date of birthday"), blank=True, null=True)
    created_at = models.DateTimeField(_("created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("update"), auto_now=True)
    gender = models.CharField(_("gender"),max_length=1, choices=GENDER_CHOICES, default="O")
    role = models.CharField(_("role"),max_length=1, choices=ROLE_CHOICES, default="U")
    notice = models.TextField(_("notice"),blank=True)
    username = models.CharField(blank=True, null=True, max_length=100)  # not use

    def get_full_name(self) -> str:
        """Return full name.

        Returns:
             str: Full name
        """
        return f"{self.first_name} {self.middle_name} {self.last_name}"

    def get_age(self) -> None | int | bool | Any:
        """Return age user.

        Returns:
            int: user age
        """
        if not self.dob:
            return
        today: date = date.today()
        return (
            today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        )

    def __str__(self) -> str:
        """Return full name."""
        return self.get_full_name()

    objects: Any = UserManager()
