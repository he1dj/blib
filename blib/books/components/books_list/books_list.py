from django.core.paginator import Paginator
from django_components import Component
from django_components import register

from blib.books.models import Book
from config.urls import books_router


@books_router.route("", name="books_list")
@register("books_list")
class BooksList(Component):
    template_name = "books_list.html"

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get("q", "")
        sort_by = request.GET.get("sort", "title")
        category_filter = request.GET.get("category", None)
        tag_filter = request.GET.get("tag", None)
        books = Book.objects.all()
        if search_query:
            books = books.filter(title__icontains=search_query)
        if category_filter:
            books = books.filter(
                book_category_relationship__category__title=category_filter,
            )
        if tag_filter:
            books = books.filter(
                book_tag_relationship__tag__title=tag_filter,
            )
        if sort_by:
            books = books.order_by(sort_by)
        paginator = Paginator(books.distinct(), 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            "books": page_obj,
            "search_query": search_query,
            "sort_by": sort_by,
            "category_filter": category_filter,
            "tag_filter": tag_filter,
        }
        return self.render_to_response(context)

    class Media:
        css = "books_list.css"
        js = "books_list.js"
