from django.urls import path

from blib.books.views import book_list
from blib.books.views import book_view

app_name = "books"

urlpatterns = [
    path("", book_list, name="books_list"),
    path("/<str:uuid>", book_view, name="book_view"),
]
