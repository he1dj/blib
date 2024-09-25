from django.shortcuts import redirect
from django_components import Component
from django_components import register

from blib.books.models import Book


@register("book_details")
class BookDetails(Component):
    template_name = "book_details.html"

    # def get_context_data(self, book):
    #     return {
    #         "book": book,
    #     }

    def get(self, request, uuid, slug=None):
        try:
            book = Book.objects.get(uuid=uuid)
            if not slug or book.slug != slug:
                return redirect("books:book_details", uuid=book.uuid, slug=book.slug)
            context = {"book": book}
            return self.render_to_response(context)
        except Book.DoesNotExist:
            return redirect("books:books_list")

    class Media:
        css = "book_details.css"
        js = "book_details.js"
