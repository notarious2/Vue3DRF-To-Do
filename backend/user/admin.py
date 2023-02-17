from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User
from .forms import CustomUserCreation


class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserCreation
    ordering = ("email",)
    list_display_links = ("email", "username")
    fieldsets = (
        (
            "Personal info",
            {
                "fields": (
                    "email",
                    "password",
                    "name",
                    "first_name",
                    "last_name",
                    "username",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    # add fields those needs to be visible when adding new user in admin.
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
