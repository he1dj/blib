from django.urls import path

from blib.books.components.book_details.book_details import BookDetails
from blib.books.components.books_list.books_list import BooksList

app_name = "books"

urlpatterns = [
    path("", BooksList.as_view(), name="books_list"),
    path("/<str:uuid>", BookDetails.as_view()),
    path("/<str:uuid>/<slug:slug>", BookDetails.as_view(), name="book_details"),
]
