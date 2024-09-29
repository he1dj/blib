from django.urls import path
from django.views.generic import TemplateView

app_name = "search"

urlpatterns = [
    path("", TemplateView.as_view(template_name="search/search.html"), name="search"),
]
