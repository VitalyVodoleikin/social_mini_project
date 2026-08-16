from django.contrib import admin

from .models import Post


@admin.register(Post)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("author", "content")
    empty_value_display = "-пусто-"
    search_fields = ("author", "content")
