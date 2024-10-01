from django.contrib import admin

from .models import Author
from .models import Book
from .models import BookAuthorRelationship
from .models import BookCategoryRelationship
from .models import BookTagRelationship
from .models import Category
from .models import Tag


class BookAuthorRelationshipInline(admin.TabularInline):
    model = BookAuthorRelationship
    extra = 1


class BookCategoryRelationshipInline(admin.TabularInline):
    model = BookCategoryRelationship
    extra = 1


class BookTagRelationshipInline(admin.TabularInline):
    model = BookTagRelationship
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "upload_date", "last_edited", "file_size")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title",)
    list_filter = ("upload_date", "last_edited")
    readonly_fields = ("qr_code", "public_url", "upload_date", "last_edited")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "slug",
                    "description",
                    "pdf",
                    "cover_image",
                    "file_size",
                ),
            },
        ),
        (
            "Links & QR",
            {
                "fields": ("public_url", "qr_code"),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("upload_date", "last_edited"),
            },
        ),
    )
    inlines = [
        BookAuthorRelationshipInline,
        BookCategoryRelationshipInline,
        BookTagRelationshipInline,
    ]

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "middle_name")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title",)
    fields = ("title",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title",)
    fields = ("title",)
