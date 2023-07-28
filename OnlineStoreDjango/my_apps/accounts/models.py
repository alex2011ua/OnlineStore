from datetime import date
from typing import Any

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, dob, password=None, **other):
        """Create user.

        Returns:
            user: new user

        """
        user = self.model(
            email=self.normalize_email(email),
            password=password,
            dob=dob,
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
            dob=timezone.now(),
            first_name="Alex",
            last_name="Kov",
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True,
        )


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []
    username: Any = models.CharField(
        blank=True,
        null=True,
        max_length=150,
        help_text=_("150 characters or fewer."),
    )
    first_name: Any = models.CharField(blank=True, null=True, max_length=100)
    last_name: Any = models.CharField(blank=True, null=True, max_length=100)
    email = models.EmailField(_("email address"), unique=True)
    dob = models.DateField(_("Date of birthday"))
    created_at = models.DateTimeField(_("created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("update"), auto_now=True)

    def get_full_name(self) -> str:
        """Return full name.

        Returns:
             str: Full name
        """
        return f"{self.first_name} {self.last_name} ({self.username})"

    def get_age(self) -> int:
        """Return age user.

        Returns:
            int: user age
        """
        today: date = date.today()
        return (
            today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        )

    def __str__(self) -> str:
        """Return full name."""
        return self.get_full_name()

    objects: Any = UserManager()
