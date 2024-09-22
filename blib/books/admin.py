from django.contrib import admin

from .models import Book
from .models import Category
from .models import Tag


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "upload_date", "last_edited", "size")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "author")
    list_filter = ("upload_date", "last_edited")
    readonly_fields = ("qr_code", "public_url", "upload_date", "last_edited")

    fieldsets = (
        (None, {
            "fields": (
                "title", "slug", "author", "description", "pdf", "cover_image", "size",
            ),
        }),
        ("Links & QR", {
            "fields": ("public_url", "qr_code"),
        }),
        ("Timestamps", {
            "fields": ("upload_date", "last_edited"),
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title",)
    fields = ("title",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title",)
    fields = ("title",)
