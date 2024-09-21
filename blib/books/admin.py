from django.contrib import admin

from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "upload_date")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "author")
    list_filter = ("upload_date",)

    readonly_fields = ("qr_code", "public_url")

    fieldsets = (
        (None, {
            "fields": ("title", "slug", "author", "description", "pdf", "cover_image"),
        }),
        ("Links & QR", {
            "fields": ("public_url", "qr_code"),
        }),
    )
