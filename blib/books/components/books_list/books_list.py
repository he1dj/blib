from django_components import Component
from django_components import register


@register("books_list")
class BooksList(Component):
    template_name = "books_list.html"

    class Media:
        css = "books_list.css"
        js = "books_list.js"
