from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.shortcuts import render

from blib.books.models import Book

# from config.urls import books_router


# @books_router.route("", name="books_list")
def books_list(request):
    books = Book.objects.all()
    paginator = Paginator(books.distinct(), 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "books": page_obj,
    }
    return render(request, "books/pages/books_list.html", context)


# @books_router.route("<str:uuid>")
# @books_router.route("<str:uuid>/<slug:slug>", name="book_details")
def book_details(request, uuid, slug):
    try:
        book = Book.objects.get(uuid=uuid)
        if not slug or book.slug != slug:
            return redirect("books:book_details", uuid=book.uuid, slug=book.slug)
        context = {"book": book}
        return render(request, "books/pages/book_details.html", context)
    except Book.DoesNotExist:
        return redirect("books:books_list")
