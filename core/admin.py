"""
core/admin.py
"""

# Import necessary modules and classes
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
from django.contrib.auth.models import Group

# Register your models here.


# Custom User Admin configuration based on the base UserAdmin
class UserAdmin(BaseUserAdmin):
    # Displayed columns in the User admin list view
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "is_superuser",
    )

    # Filter options for the User admin list view
    list_filter = ("is_superuser",)

    # Ordering options for the User admin list view
    ordering = ("id",)

    # Fieldsets configuration for the User admin detail view
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal Info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        ("Permissions", {"fields": ("is_superuser",)}),
    )

    # Add fieldsets configuration for adding a new User in the admin
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


# Unregister the default Group model from the admin (not needed in this case)
admin.site.unregister(Group)

# Register the custom User model with the custom UserAdmin
admin.site.register(User, UserAdmin)
