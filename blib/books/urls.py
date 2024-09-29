from django.urls import path

from blib.books.views import BookDetailView
from blib.books.views import BookListView

app_name = "books"

urlpatterns = [
    path("", BookListView.as_view(), name="books_list"),
    path("/<str:uuid>", BookDetailView.as_view()),
    path("/<str:uuid>/<slug:slug>", BookDetailView.as_view(), name="book_details"),
]
