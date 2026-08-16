from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active"
    )
    search_fields = ("username", "email")
    list_filter = ("first_name", "last_name")
    ordering = ("username",)
    empty_value_display = "-пусто-"
