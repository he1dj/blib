from django.urls import path
from django.views.generic import TemplateView

app_name = "books"

urlpatterns = [
    path("", TemplateView.as_view(template_name="books/pages/home.html"), name="books_home"),
]
