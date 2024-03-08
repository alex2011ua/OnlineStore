import uuid
from datetime import date
from typing import Any, ClassVar

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


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


class User(AbstractUser):  # type: ignore
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    GENDER_CHOICES = [
        ("M", "male"),
        ("F", "female"),
        ("O", "other"),
    ]
    ROLE_CHOICES = [
        ("A", "admin"),
        ("M", "manager"),
        ("U", "auth_user"),
    ]
    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = []

    first_name = models.CharField(
        _("first name"),
        name="first_name",
        max_length=100,
        blank=True,
        null=True,
    )  # type: ignore
    middle_name = models.CharField(
        _("middle name"), blank=True, null=True, max_length=100
    )  # type: ignore
    last_name = models.CharField(_("last name"), blank=True, null=True, max_length=100)  # type: ignore

    email = models.EmailField(_("email address"), unique=True)
    mobile = PhoneNumberField(null=True, blank=True, unique=True)

    address = models.CharField(_("delivery address"), max_length=255, blank=True)
    dob = models.DateField(_("Date of birthday"), blank=True, null=True)
    created_at = models.DateTimeField(_("created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("update"), auto_now=True)
    gender = models.CharField(_("gender"), max_length=1, choices=GENDER_CHOICES, default="O")
    role = models.CharField(_("role"), max_length=1, choices=ROLE_CHOICES, default="U")
    notice = models.TextField(_("notice"), blank=True)
    username = models.CharField(blank=True, null=True, max_length=100)  # type: ignore

    def get_full_name(self) -> str:
        """Return full name.

        Returns:
             str: Full name
        """
        return f"{self.first_name} {self.middle_name if self.middle_name else ''} {self.last_name}"  # type: ignore

    def get_age(self) -> None | int:
        """Return age user.

        Returns:
            int: user age
            None: not in db
        """
        if not self.dob:
            return 0
        today: date = date.today()
        return (
            today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        )

    def __str__(self) -> str:
        """Return full name."""
        return self.get_full_name()

    objects = UserManager()  # type: ignore
