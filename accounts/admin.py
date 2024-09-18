from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "is_staff", "is_active", "is_superuser", 'id', 'is_verified')
    list_filter = ("email", "is_staff", "is_active", "is_superuser" , 'is_verified')
    search_fields = ("email",)
    ordering = ("email",)
    fieldsets = (
        ("Authentication", {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", 'is_verified',  "user_permissions", "groups")}),
        ("import date", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        ("َAdd User", {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "is_superuser", "groups", "user_permissions", "is_verified"
            )}
         ),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)