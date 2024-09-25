from django.urls import path

from blib.books.views import book_details
from blib.books.views import books_list

app_name = "books"

urlpatterns = [
    path("", books_list, name="books_list"),
    path("/<str:uuid>/<slug:slug>", book_details, name="book_details"),
    path("/<str:uuid>", book_details),
]
