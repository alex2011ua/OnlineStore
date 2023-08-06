from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from my_apps.accounts.form import UserChangeForm, UserCreationForm
from my_apps.accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
    "first_name", "middle_name", "last_name", "email", "password", "mobile", "gender", "role", "notice", "created_at",
    "updated_at")
    list_filter = ("dob", "created_at", "gender")
    fieldsets = (
        (None, {"fields": ("email", "password", "mobile")}),
        ("Personal info", {"fields": ("first_name", "middle_name", "last_name")}),
        ("Some info", {"fields": ("gender", "role", "notice",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "dob", "password1", "password2"),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.unregister(Group)
