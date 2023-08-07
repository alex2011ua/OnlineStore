from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from my_apps.accounts.models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users(in admin and other)."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        """Class Meta."""

        model = User
        fields = ("email", "username", "first_name", "last_name")

    def clean_password2(self):
        """Check that the two password entries match."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """Save the provided password in hashed format."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password1"))
        user.last_name = self.cleaned_data.get("last_name")
        user.first_name = self.cleaned_data.get("first_name")

        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users."""

    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            'You can change the password using <a href="../password">this form</a>.'
        ),
    )

    class Meta:
        """Class Meta."""

        model = User
        fields = "__all__"
