from django.core.paginator import Paginator
from django_components import Component
from django_components import register

from blib.books.models import Book


@register("books_list")
class BooksList(Component):
    template_name = "books_list.html"

    def get(self, request):
        books = Book.objects.all()
        paginator = Paginator(books.distinct(), 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            "books": page_obj,
        }
        return self.render_to_response(context)

    class Media:
        css = "books_list.css"
        js = "books_list.js"
