
from django_components import Component
from django_components import register


@register("book_list")
class BookListComponent(Component):
    template_name = "book_list.html"

    class Media:
        css = "book_list.css"
        js = "book_list.js"
