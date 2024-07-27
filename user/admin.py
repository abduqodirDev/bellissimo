from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from user.models import User, UserConfirmation


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password", "phone_number", "date_of_birth")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "password1", "password2"),
            },
        ),
    )

    list_display = ("phone_number", "username", "first_name", "is_staff", "is_active")
    search_fields = ("phone_number", 'username', "first_name", "last_name", "email")
    ordering = ("-created_time",)
    list_display_links = ('username', 'phone_number')


@admin.register(UserConfirmation)
class UserConfirmationAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'status')
    list_filter = ['user', 'status']
    search_fields = ('user', 'code')
