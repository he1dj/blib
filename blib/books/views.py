from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.shortcuts import render

from django_routify import Router

from .models import Book

books_router = Router("/books", "books", auto_trailing_slash=False)


@books_router.route("", name="books_list")
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
    return render(request, "books/pages/home.html", context)


@books_router.route("/<str:uuid>")
@books_router.route("/<str:uuid>/<slug:slug>", name="book_view")
def book_view(request, uuid, slug=None):
    try:
        book = Book.objects.get(uuid=uuid)
        if not slug or book.slug != slug:
            return redirect("books:book_view", uuid=book.uuid, slug=book.slug)
        context = {"book": book}
        return render(request, "books/pages/book.html", context)
    except Book.DoesNotExist:
        return redirect("books:books_home")
