from django.urls import path

from blib.books.views import book_list

app_name = "books"

urlpatterns = [
    path("", book_list, name="books_home"),
]
