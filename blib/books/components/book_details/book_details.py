from django.shortcuts import redirect
from django_components import Component
from django_components import register

from blib.books.models import Book
from blib.books.urls import books_router


@books_router.route("/<str:uuid>")
@books_router.route("/<str:uuid>/<slug:slug>", name="book_view")
@register("book_details")
class BookDetails(Component):
    template_name = "book_details.html"

    # def get_context_data(self, book):
    #     return {
    #         "book": book,
    #     }

    def get(self, request, *args, **kwargs):
        uuid = kwargs.get("uuid")
        slug = kwargs.get("slug", None)
        try:
            book = Book.objects.get(uuid=uuid)
            slug = kwargs.get("slug", None)
            if not slug or book.slug != slug:
                return redirect("books:book_view", uuid=book.uuid, slug=book.slug)
            context = {"book": book}
            return self.render_to_response(context)
        except Book.DoesNotExist:
            return redirect("books:books_list")

    class Media:
        css = "book_details.css"
        js = "book_details.js"
