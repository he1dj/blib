from django.templatetags.static import static
from django.utils.html import format_html
from wagtail import hooks


@hooks.register("insert_editor_js")
def editor_js():
    return format_html(
        '<script src="https://cdn.jsdelivr.net/npm/slugify@1.6.6/slugify.min.js"></script>'
        '<script src="{}"></script>', static("books/js/slug-auto-fill.js"),
    )
