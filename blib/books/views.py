from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Book


def book_list(request):
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
        books = books.filter(book_tag_relationship__tag__title=tag_filter)
    if sort_by:
        books = books.order_by(sort_by)
    paginator = Paginator(books, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "books": page_obj,
        # "search_query": search_query,
        # "sort_by": sort_by,
        # "category_filter": category_filter,
        # "tag_filter": tag_filter,
    }
    return render(request, "books/pages/home.html", context)
